#!/usr/bin/env node
/**
 * TheBhom Automated Visual & Console Verification Gate (Chrome CDP)
 * 
 * Directly attaches to Apple Silicon Chrome Remote Debugging (port 9222)
 * via Chrome DevTools Protocol (CDP) WebSocket.
 * 
 * Verifies:
 * 1. Zero JavaScript runtime exceptions (Runtime.exceptionThrown)
 * 2. Zero 4xx/5xx network asset failures (scripts, css, fonts, images)
 * 3. Zero broken <img> tags (naturalWidth > 0 check)
 * 4. High-resolution visual snapshot capture (.verify_snapshots/)
 * 
 * Usage:
 *   node scripts/verify_visual_cdp.mjs https://www.thebhom.in/
 *   node scripts/verify_visual_cdp.mjs https://www.thebhom.in/guides/youtube-video-kaise-download-kare-gallery-me
 */

import fs from 'node:fs';
import path from 'node:path';

const CDP_HOST = 'http://127.0.0.1:9222';
const SNAPSHOT_DIR = path.resolve('.verify_snapshots');

if (!fs.existsSync(SNAPSHOT_DIR)) {
  fs.mkdirSync(SNAPSHOT_DIR, { recursive: true });
}

async function verifyPage(url) {
  console.log(`\n======================================================`);
  console.log(`🔍 [CDP Verification Gate] Checking: ${url}`);
  console.log(`======================================================`);

  // 1. Create a new background tab in Chrome via CDP HTTP API
  const newTabRes = await fetch(`${CDP_HOST}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
  if (!newTabRes.ok) {
    throw new Error(`Failed to create Chrome tab on ${CDP_HOST}. Is Chrome running with --remote-debugging-port=9222?`);
  }
  const tab = await newTabRes.json();
  const tabId = tab.id;
  const wsUrl = tab.webSocketDebuggerUrl;

  const runtimeErrors = [];
  const networkErrors = [];
  const consoleWarnings = [];

  return new Promise((resolve) => {
    const ws = new WebSocket(wsUrl);
    let msgId = 1;
    const pendingCallbacks = new Map();

    function send(method, params = {}) {
      return new Promise((res, rej) => {
        const id = msgId++;
        pendingCallbacks.set(id, { res, rej });
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    ws.onopen = async () => {
      try {
        // Enable essential CDP domains
        await send('Runtime.enable');
        await send('Log.enable');
        await send('Network.enable');
        await send('Page.enable');

        // Wait for page load and settle
        await new Promise((r) => setTimeout(r, 3500));

        // Evaluate DOM integrity & broken images inside the real page
        const evalRes = await send('Runtime.evaluate', {
          expression: `(() => {
            const brokenImages = Array.from(document.querySelectorAll('img'))
              .filter(img => img.src && (!img.complete || img.naturalWidth === 0))
              .map(img => img.src);
            
            return {
              title: document.title,
              textLength: document.body ? document.body.innerText.length : 0,
              brokenImages: brokenImages,
              hasH1: !!document.querySelector('h1'),
              canonical: document.querySelector('link[rel="canonical"]')?.href || null
            };
          })()`,
          returnByValue: true
        });

        const domMetrics = evalRes?.result?.value || {};

        // Capture full-page visual screenshot
        const screenshotRes = await send('Page.captureScreenshot', {
          format: 'png',
          captureBeyondViewport: false
        });

        const safeName = url.replace(/https?:\/\//, '').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 50);
        const snapshotFile = path.join(SNAPSHOT_DIR, `${safeName}.png`);
        
        if (screenshotRes?.data) {
          fs.writeFileSync(snapshotFile, Buffer.from(screenshotRes.data, 'base64'));
        }

        // Close tab via CDP HTTP API
        await fetch(`${CDP_HOST}/json/close/${tabId}`);
        ws.close();

        // Print Verification Report
        console.log(`📄 Document Title: "${domMetrics.title || 'N/A'}"`);
        console.log(`🔗 Canonical URL: ${domMetrics.canonical || 'None'}`);
        console.log(`📝 Text Density: ${domMetrics.textLength} characters`);
        console.log(`📸 Visual Snapshot: ${snapshotFile}`);

        let passed = true;

        if (runtimeErrors.length > 0) {
          passed = false;
          console.log(`\n❌ [FAILED] Runtime JavaScript Exceptions (${runtimeErrors.length}):`);
          runtimeErrors.forEach(err => console.log(`   • ${err}`));
        } else {
          console.log(`✅ Runtime JavaScript: 0 uncaught exceptions`);
        }

        if (networkErrors.length > 0) {
          // Allow tracking/analytics warnings but fail on critical assets
          const criticalErrors = networkErrors.filter(e => !e.url.includes('google-analytics') && !e.url.includes('pagead2'));
          if (criticalErrors.length > 0) {
            passed = false;
            console.log(`\n❌ [FAILED] Critical Network Asset Failures (${criticalErrors.length}):`);
            criticalErrors.forEach(e => console.log(`   • [${e.status}] ${e.url}`));
          } else {
            console.log(`✅ Critical Assets: 100% loaded successfully`);
          }
        } else {
          console.log(`✅ Network Status: 0 asset failures`);
        }

        if (domMetrics.brokenImages && domMetrics.brokenImages.length > 0) {
          passed = false;
          console.log(`\n❌ [FAILED] Broken Image Elements Found (${domMetrics.brokenImages.length}):`);
          domMetrics.brokenImages.forEach(img => console.log(`   • ${img}`));
        } else {
          console.log(`✅ Image Assets: 0 broken images detected`);
        }

        if (passed) {
          console.log(`\n🎉 [VERIFICATION PASSED] Page is 100% production-healthy!`);
          resolve(true);
        } else {
          console.log(`\n🚨 [VERIFICATION FAILED] Issues detected in browser execution.`);
          resolve(false);
        }
      } catch (err) {
        console.error('Error during CDP verification:', err);
        try { await fetch(`${CDP_HOST}/json/close/${tabId}`); } catch (_) {}
        resolve(false);
      }
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.id && pendingCallbacks.has(msg.id)) {
          const { res, rej } = pendingCallbacks.get(msg.id);
          pendingCallbacks.delete(msg.id);
          if (msg.error) rej(msg.error);
          else res(msg.result);
        }

        // Intercept runtime exceptions
        if (msg.method === 'Runtime.exceptionThrown') {
          const desc = msg.params?.exceptionDetails?.exception?.description || msg.params?.exceptionDetails?.text || 'Unknown exception';
          runtimeErrors.push(desc);
        }

        // Intercept console errors
        if (msg.method === 'Log.entryAdded' && msg.params?.entry?.level === 'error') {
          runtimeErrors.push(`[Console Error] ${msg.params.entry.text}`);
        }

        // Intercept network failures
        if (msg.method === 'Network.responseReceived') {
          const resp = msg.params?.response;
          if (resp && resp.status >= 400) {
            networkErrors.push({ url: resp.url, status: resp.status });
          }
        }
      } catch (e) {
        // Ignore json parse error
      }
    };

    ws.onerror = async (err) => {
      console.error('WebSocket error:', err);
      try { await fetch(`${CDP_HOST}/json/close/${tabId}`); } catch (_) {}
      resolve(false);
    };
  });
}

async function main() {
  const targetUrl = process.argv[2] || 'https://www.thebhom.in/';
  const ok = await verifyPage(targetUrl);
  process.exit(ok ? 0 : 1);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
