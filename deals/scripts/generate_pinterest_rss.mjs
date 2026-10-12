#!/usr/bin/env node
/**
 * Pinterest RSS Feed Generator for TheBhom Deals
 * Creates fully compliant RSS 2.0 + Media RSS feeds optimized for Pinterest Auto-Publishing.
 *
 * Features:
 * - High-SEO Titles with discount tags (<100 chars)
 * - Rich SEO descriptions with deal specs and high-converting hashtags
 * - 1500px High-Definition Amazon image enclosures
 * - Clean URLs linking to dedicated product detail pages (deals/p/{slug})
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DEALS_DIR = path.resolve(__dirname, '..');
const CATALOG_PATH = path.join(DEALS_DIR, 'data', 'catalog.json');
const FEEDS_DIR = path.join(DEALS_DIR, 'feeds');

if (!fs.existsSync(FEEDS_DIR)) {
  fs.mkdirSync(FEEDS_DIR, { recursive: true });
}

function escapeXml(unsafe) {
  if (!unsafe) return '';
  return String(unsafe)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function getHdImageUrl(url) {
  if (!url) return '';
  // Replace Amazon thumbnail modifiers with high-resolution 1500px version
  return url.replace(/\._[A-Za-z0-9_,-]+_\.jpg$/i, '._SL1500_.jpg');
}

function buildSeoTitle(item) {
  let title = item.title || 'Trendy Fashion Deal';
  title = title.replace(/\s+/g, ' ').trim();
  
  const discount = item.discount || (item.discountNum ? `${item.discountNum}% OFF` : '');
  const prefix = discount ? `[${discount}] ` : '';
  
  let cleanTitle = title;
  const maxTitleLen = 95 - prefix.length;
  if (cleanTitle.length > maxTitleLen) {
    cleanTitle = cleanTitle.substring(0, maxTitleLen - 3).trim() + '...';
  }
  
  return `${prefix}${cleanTitle}`;
}

function buildSeoDescription(item) {
  const title = item.title || 'Product Deal';
  const price = item.price ? `₹${item.price}` : '';
  const mrp = item.mrp ? `₹${item.mrp}` : '';
  const discount = item.discount || (item.discountNum ? `${item.discountNum}% OFF` : '');
  const subcategory = item.subcategory || item.category || 'Fashion';
  
  let desc = `🔥 ${title}\n\n`;
  desc += `✨ Special Deal Price: ${price} ${mrp ? `(MRP: ${mrp})` : ''} - Save ${discount}!\n`;
  desc += `🛍️ Category: ${subcategory} | Verified Amazon Deal\n`;
  desc += `⚡ Limited Time Price Drop! Tap the link below to grab this deal on TheBhom Deals before the sale ends!\n\n`;
  
  // High SEO hashtags
  const hashtags = [
    '#WomensFashion',
    '#EthnicWear',
    '#AmazonDeals',
    '#LootDeals',
    '#FashionTrends',
    '#OOTD',
    '#TrendingStyle',
    '#FestiveWear',
    '#IndianFashion',
    '#OnlineShopping'
  ];
  
  if (title.toLowerCase().includes('saree')) hashtags.push('#SareeLove', '#SareesOnline');
  if (title.toLowerCase().includes('kurti')) hashtags.push('#KurtiDesign', '#Chikankari');
  if (title.toLowerCase().includes('dress')) hashtags.push('#DressesOnline', '#PartyWear');
  if (title.toLowerCase().includes('jeans')) hashtags.push('#DenimStyle', '#JeansFit');
  if (title.toLowerCase().includes('top')) hashtags.push('#CropTops', '#Styling');

  desc += hashtags.slice(0, 8).join(' ');
  return desc;
}

function generateRssXml({ title, link, description, items }) {
  const pubDate = new Date().toUTCString();
  
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">\n`;
  xml += `  <channel>\n`;
  xml += `    <title>${escapeXml(title)}</title>\n`;
  xml += `    <link>${escapeXml(link)}</link>\n`;
  xml += `    <description>${escapeXml(description)}</description>\n`;
  xml += `    <language>en-in</language>\n`;
  xml += `    <lastBuildDate>${pubDate}</lastBuildDate>\n`;
  xml += `    <atom:link href="${escapeXml(link)}" rel="self" type="application/rss+xml" />\n`;

  for (const item of items) {
    const seoTitle = buildSeoTitle(item);
    const seoDesc = buildSeoDescription(item);
    const productUrl = `https://thebhom.in/deals/p/${item.slug || item.id}`;
    const hdImg = getHdImageUrl(item.image);
    const guid = `thebhom-deal-${item.id || item.asin || item.slug}`;
    
    xml += `    <item>\n`;
    xml += `      <title>${escapeXml(seoTitle)}</title>\n`;
    xml += `      <link>${escapeXml(productUrl)}</link>\n`;
    xml += `      <description>${escapeXml(seoDesc)}</description>\n`;
    xml += `      <guid isPermaLink="false">${escapeXml(guid)}</guid>\n`;
    xml += `      <pubDate>${pubDate}</pubDate>\n`;
    if (hdImg) {
      xml += `      <enclosure url="${escapeXml(hdImg)}" type="image/jpeg" length="150000" />\n`;
      xml += `      <media:content url="${escapeXml(hdImg)}" medium="image" width="1000" height="1500" />\n`;
      xml += `      <media:thumbnail url="${escapeXml(hdImg)}" />\n`;
    }
    xml += `    </item>\n`;
  }

  xml += `  </channel>\n`;
  xml += `</rss>\n`;
  return xml;
}

async function main() {
  console.log('Loading catalog from:', CATALOG_PATH);
  const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf-8'));
  console.log(`Loaded ${catalog.length} total products.`);

  // Deduplication helper by ASIN/Title
  function dedupe(items) {
    const seen = new Set();
    const result = [];
    for (const p of items) {
      const key = (p.asin || p.pid || p.title.substring(0, 30)).toLowerCase().trim();
      if (!seen.has(key)) {
        seen.add(key);
        result.push(p);
      }
    }
    return result;
  }

  // 1. Filter Women's Fashion deals (Realistic high-converting prices & discounts)
  const womenItems = catalog.filter(p => {
    const isWomen = p.department === 'women' || 
           (p.category === 'fashion' && (
             /saree|kurti|dress|jeans|top|suit|anarkali|sharara|ethnic|women|girl/i.test(p.title) ||
             /women/i.test(p.department || '')
           ));
    const validPrice = p.price >= 149 && p.price <= 9999;
    const validDiscount = (p.discountNum >= 30 && p.discountNum <= 90) || !p.discountNum;
    return isWomen && validPrice && validDiscount;
  });

  const dedupedWomen = dedupe(womenItems);
  dedupedWomen.sort((a, b) => (b.discountNum || 0) - (a.discountNum || 0));
  const topWomen = dedupedWomen.slice(0, 250); // Optimal feed length for Pinterest

  console.log(`Filtered ${womenItems.length} women's items (${dedupedWomen.length} unique). Using top ${topWomen.length} for Women's Fashion feed.`);

  const womenXml = generateRssXml({
    title: "TheBhom Women's Fashion & Ethnic Wear Deals",
    link: "https://thebhom.in/deals/feeds/pinterest-women-fashion.xml",
    description: "Trending verified Amazon deals on sarees, kurtis, dresses, tops, and ethnic wear with up to 90% discount.",
    items: topWomen
  });

  const womenFeedPath = path.join(FEEDS_DIR, 'pinterest-women-fashion.xml');
  fs.writeFileSync(womenFeedPath, womenXml, 'utf-8');
  console.log(`Saved Women's Fashion RSS feed to: ${womenFeedPath} (${(womenXml.length / 1024).toFixed(1)} KB)`);

  // 2. All Deals Feed (Top highest discount deals across all categories)
  const validAll = catalog.filter(p => {
    const validPrice = p.price >= 99 && p.price <= 49999;
    const validDiscount = (p.discountNum >= 40 && p.discountNum <= 92) || !p.discountNum;
    return validPrice && validDiscount;
  });
  const dedupedAll = dedupe(validAll);
  dedupedAll.sort((a, b) => (b.discountNum || 0) - (a.discountNum || 0));
  const topAll = dedupedAll.slice(0, 250);

  const allDealsXml = generateRssXml({
    title: "TheBhom Daily Loot Deals & Mega Price Drops",
    link: "https://thebhom.in/deals/feeds/pinterest-all-deals.xml",
    description: "Verified Amazon & Flipkart mega price drops, flash sales, and top discount deals updated daily.",
    items: topAll
  });

  const allDealsFeedPath = path.join(FEEDS_DIR, 'pinterest-all-deals.xml');
  fs.writeFileSync(allDealsFeedPath, allDealsXml, 'utf-8');
  console.log(`Saved All Deals RSS feed to: ${allDealsFeedPath} (${(allDealsXml.length / 1024).toFixed(1)} KB)`);

  // Also create root aliases in /deals/ for clean easy URLs
  fs.writeFileSync(path.join(DEALS_DIR, 'rss-women.xml'), womenXml, 'utf-8');
  fs.writeFileSync(path.join(DEALS_DIR, 'rss.xml'), allDealsXml, 'utf-8');
  console.log('Created root aliases: deals/rss-women.xml and deals/rss.xml');
}

main().catch(err => {
  console.error('Fatal error generating Pinterest RSS feeds:', err);
  process.exit(1);
});
