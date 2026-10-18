// Cloudflare Pages Function: /api/parse
// Highly Advanced, Self-Healing Universal Video Downloader Engine
// Supports YouTube, TikTok, Instagram, Facebook, Pinterest, Reddit, Dailymotion, Twitter/X
// Features: Dynamic Auth Scraping, AES-256-CBC Auto-Decryption, and Asynchronous SSE Stream Resolution

import CryptoJS from "crypto-js";

// Cached in-memory tokens across warm worker invocations
let TOKEN_CACHE = {
  auth: "4c9b7d21",
  aesKey: "4c9b7d2e4c9b7d2e4c9b7d2e4c9b7d21",
  domain: "api-ak.vidssave.com",
  timestamp: 0
};

const VIDSSAVE_PARSE_API = "https://api.vidssave.com/api/contentsite_api/media/parse";
const VIDSSAVE_DOWNLOAD_API = "https://api.vidssave.com/api/contentsite_api/media/download";
const VIDSSAVE_SSE_BASE = "https://api.vidssave.com/sse/contentsite_api/media/download_query";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json; charset=utf-8"
  };
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: corsHeaders() });
}

function detectPlatform(url) {
  const u = (url || "").toLowerCase();
  if (u.includes("youtube.com") || u.includes("youtu.be")) return "youtube";
  if (u.includes("instagram.com")) return "instagram";
  if (u.includes("tiktok.com")) return "tiktok";
  if (u.includes("facebook.com") || u.includes("fb.watch")) return "facebook";
  if (u.includes("twitter.com") || u.includes("x.com")) return "twitter";
  if (u.includes("pinterest.com") || u.includes("pin.it")) return "pinterest";
  if (u.includes("reddit.com") || u.includes("redd.it")) return "reddit";
  if (u.includes("dailymotion.com") || u.includes("dai.ly")) return "dailymotion";
  return "general";
}

// AES-256-CBC ZeroPadding Decryption matching VidsSave client algorithm
function decryptVidsSave(ciphertextB64, keyStr = "4c9b7d2e4c9b7d2e4c9b7d2e4c9b7d21") {
  try {
    const key = CryptoJS.enc.Utf8.parse(keyStr);
    const iv = CryptoJS.enc.Utf8.parse(keyStr.slice(0, 16));
    const cipherParams = CryptoJS.lib.CipherParams.create({
      ciphertext: CryptoJS.enc.Base64.parse(ciphertextB64)
    });
    const decrypted = CryptoJS.AES.decrypt(cipherParams, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.ZeroPadding
    });
    const str = decrypted.toString(CryptoJS.enc.Utf8).replace(/\0+$/, "");
    return JSON.parse(str);
  } catch (err) {
    // Fallback to secondary key if primary failed
    try {
      const fallbackKey = "rz18efAXUbdiaO7k";
      const key = CryptoJS.enc.Utf8.parse(fallbackKey);
      const iv = CryptoJS.enc.Utf8.parse(fallbackKey.slice(0, 16));
      const cipherParams = CryptoJS.lib.CipherParams.create({
        ciphertext: CryptoJS.enc.Base64.parse(ciphertextB64)
      });
      const decrypted = CryptoJS.AES.decrypt(cipherParams, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.ZeroPadding
      });
      const str = decrypted.toString(CryptoJS.enc.Utf8).replace(/\0+$/, "");
      return JSON.parse(str);
    } catch (e2) {
      return null;
    }
  }
}

// Dynamically scrapes latest auth token and AES key from VidsSave Next.js bundle
async function refreshLiveTokens() {
  try {
    const htmlResp = await fetch("https://vidssave.com/youtube-video-downloader-8hs", {
      headers: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      }
    });
    if (!htmlResp.ok) return;

    const html = await htmlResp.text();
    const scripts = [...html.matchAll(/<script[^>]*src=["']([^"']+)["'][^>]*>/g)].map(m => m[1]);

    for (const scriptUrl of scripts) {
      if (!scriptUrl.includes("/chunks/")) continue;
      // Fetch layout or site chunks
      if (scriptUrl.includes("layout-") || scriptUrl.includes("1074-") || scriptUrl.includes("6215-")) {
        const jsResp = await fetch(scriptUrl);
        if (!jsResp.ok) continue;
        const js = await jsResp.text();

        if (js.includes("auth:")) {
          const authMatch = js.match(/auth:["']([a-f0-9]+)["']/);
          const keyMatch = js.match(/\[["']([a-f0-9]{8})["']\.repeat\(3\)\.concat\(["']([a-f0-9]{8})["']\)/);
          const domainMatch = js.match(/VIDEODOWNLOAD:["']([^"']+)["']/);

          if (authMatch && keyMatch) {
            TOKEN_CACHE = {
              auth: authMatch[1],
              aesKey: keyMatch[1].repeat(3) + keyMatch[2],
              domain: domainMatch ? domainMatch[1] : "api-ak.vidssave.com",
              timestamp: Date.now()
            };
            return;
          }
        }
      }
    }
  } catch (e) {
    // If scrape fails, keep existing cache
  }
}

async function getTokens() {
  const now = Date.now();
  // Refresh cache every 6 hours
  if (!TOKEN_CACHE.timestamp || (now - TOKEN_CACHE.timestamp) > 6 * 3600 * 1000) {
    await refreshLiveTokens();
  }
  return TOKEN_CACHE;
}

// Calls primary parse API
async function callVidsSaveParse(url, origin = "source", tokens) {
  const payload = new URLSearchParams({
    hostname: "vidssave.com",
    auth: tokens.auth,
    domain: tokens.domain || "api-ak.vidssave.com",
    link: url.trim(),
    origin: origin
  });

  const res = await fetch(VIDSSAVE_PARSE_API, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Referer": "https://vidssave.com/",
      "Origin": "https://vidssave.com"
    },
    body: payload.toString()
  });

  if (!res.ok) return null;
  return await res.json().catch(() => null);
}

// Resolves 2nd stage download link via media/download and SSE stream query
async function resolveStreamDownloadUrl(resourceContent, tokens) {
  try {
    const dlPayload = new URLSearchParams({
      hostname: "vidssave.com",
      auth: tokens.auth,
      domain: tokens.domain || "api-ak.vidssave.com",
      request: resourceContent,
      no_encrypt: "1"
    });

    const dlResp = await fetch(VIDSSAVE_DOWNLOAD_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://vidssave.com/",
        "Origin": "https://vidssave.com"
      },
      body: dlPayload.toString()
    });

    if (!dlResp.ok) return null;
    const dlJson = await dlResp.json();
    if (!dlJson || dlJson.status !== 1) return null;

    const dlData = typeof dlJson.data === "string" ? decryptVidsSave(dlJson.data, tokens.aesKey) : dlJson.data;
    if (!dlData || !dlData.task_id) return null;

    const sseUrl = `${VIDSSAVE_SSE_BASE}?auth=20250901majwlqo&domain=${encodeURIComponent(tokens.domain || "api-ak.vidssave.com")}&task_id=${encodeURIComponent(dlData.task_id)}&download_domain=vidssave.com&origin=content_site`;

    const sseResp = await fetch(sseUrl, {
      headers: {
        "Accept": "text/event-stream",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://vidssave.com/"
      }
    });

    if (!sseResp.ok || !sseResp.body) return null;

    const reader = sseResp.body.getReader();
    const decoder = new TextDecoder();
    let downloadLink = null;

    // Read initial stream chunk (usually arrives within 1-2 seconds with 100% progress)
    for (let i = 0; i < 4; i++) {
      const { value, done } = await reader.read();
      if (done) break;
      if (value) {
        const chunk = decoder.decode(value);
        const match = chunk.match(/"download_link":"([^"]+)"/);
        if (match && match[1]) {
          downloadLink = match[1].replace(/\\u0026/g, "&");
          break;
        }
      }
    }
    reader.cancel().catch(() => {});
    return downloadLink;
  } catch (e) {
    return null;
  }
}

export async function onRequestPost(context) {
  try {
    const { request } = context;
    const body = await request.json().catch(() => ({}));
    const rawUrl = (body.url || "").trim();

    if (!rawUrl) {
      return new Response(JSON.stringify({ status: "error", error: "Missing video URL" }), {
        status: 400,
        headers: corsHeaders()
      });
    }

    let tokens = await getTokens();

    // 1. Try parsing with active tokens
    let apiResp = await callVidsSaveParse(rawUrl, "source", tokens);

    // If parse failed, tokens might have rotated! Force dynamic refresh and retry
    if (!apiResp || apiResp.status !== 1) {
      await refreshLiveTokens();
      tokens = TOKEN_CACHE;
      apiResp = await callVidsSaveParse(rawUrl, "source", tokens);
    }

    if (apiResp && apiResp.status === 1 && apiResp.data) {
      let raw = apiResp.data;
      if (typeof raw === "string") {
        raw = decryptVidsSave(raw, tokens.aesKey);
      }

      if (raw && raw.resources && raw.resources.length > 0) {
        const rawResources = raw.resources;

        // Resolve direct download URLs in parallel for formats that need 2-stage muxing
        const resolvedResources = await Promise.all(
          rawResources.map(async (r) => {
            let dlUrl = r.download_url || "";
            if (!dlUrl && r.resource_content) {
              dlUrl = await resolveStreamDownloadUrl(r.resource_content, tokens);
            }

            const isAudio = r.type === "audio" || (r.format || "").toUpperCase() === "MP3" || (r.quality || "").toUpperCase().includes("KBPS");

            return {
              format: (r.format || (isAudio ? "MP3" : "MP4")).toUpperCase(),
              quality: r.quality || "HD",
              size_bytes: r.size || 0,
              download_url: dlUrl || "",
              type: isAudio ? "audio" : "video"
            };
          })
        );

        // Filter out formats that failed completely
        const validResources = resolvedResources.filter(r => r.download_url);

        if (validResources.length > 0) {
          return new Response(
            JSON.stringify({
              status: "success",
              data: {
                engine: "vidssave",
                title: raw.title || "Online Video",
                duration_sec: raw.duration || 0,
                thumbnail: raw.thumbnail || "",
                author: raw.author || raw.user_item?.nickname || "Creator",
                resources: validResources,
                platform: detectPlatform(rawUrl)
              }
            }),
            { status: 200, headers: corsHeaders() }
          );
        }
      }
    }

    // High-bandwidth fallback gateway if stream was protected
    const platform = detectPlatform(rawUrl);
    return new Response(
      JSON.stringify({
        status: "fallback",
        platform: platform,
        url: rawUrl,
        message: `Direct cloud stream extraction for ${platform.toUpperCase()} was protected. Please use local companion or 1-click gateway.`
      }),
      { status: 200, headers: corsHeaders() }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ status: "error", error: err.message || "Failed to parse video" }),
      { status: 500, headers: corsHeaders() }
    );
  }
}
