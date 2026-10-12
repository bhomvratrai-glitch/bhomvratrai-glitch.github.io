#!/usr/bin/env node
/**
 * Pinterest-Native SEO RSS Feed Generator for TheBhom Deals
 * 
 * Specifically engineered for Pinterest Guided Search & Taste Graph Algorithm:
 * - Zero spammy "Loot/Discounts" clickbait titles (which Pinterest algorithm downranks).
 * - Aesthetic styling hooks, lookbooks, outfit recommendations, and wardrobe essentials.
 * - Saves-driving CTA ("Save this pin to your Outfit Inspo board") — saves are Pinterest's #1 ranking signal.
 * - 1500px Ultra HD studio imagery without text stickers.
 * - Natural contextual keywords that rank on Pinterest search:
 *   "aesthetic outfits", "styling guide", "lookbook", "wedding guest inspo", "amazon fashion finds".
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
  return url.replace(/\._[A-Za-z0-9_,-]+_\.jpg$/i, '._SL1500_.jpg');
}

// Classify product type for targeted Pinterest search intent
function detectFashionCategory(title, subcategory = '') {
  const t = (title + ' ' + subcategory).toLowerCase();
  if (t.includes('saree')) return 'saree';
  if (t.includes('chikankari') || t.includes('kurti') || t.includes('anarkali') || t.includes('sharara') || t.includes('salwar') || t.includes('suit set')) return 'ethnic';
  if (t.includes('jeans') || t.includes('denim') || t.includes('bootcut') || t.includes('flared') || t.includes('baggy')) return 'jeans';
  if (t.includes('trouser') || t.includes('cargo') || t.includes('pant') || t.includes('pleated')) return 'trousers';
  if (t.includes('dress') || t.includes('gown') || t.includes('maxi') || t.includes('slip') || t.includes('bodycon')) return 'dress';
  if (t.includes('top') || t.includes('crop') || t.includes('shirt') || t.includes('tee') || t.includes('corset') || t.includes('blouse')) return 'top';
  if (t.includes('co-ord') || t.includes('coord') || t.includes('set')) return 'coord';
  return 'fashion';
}

function cleanProductCoreName(title) {
  // Strip out vendor noise like "|| Latest Stylish Summer Tops..."
  let clean = title.split('||')[0].split('|')[0].trim();
  clean = clean.replace(/^(sponsored\s*[:-]?\s*)/i, '');
  clean = clean.replace(/\s+/g, ' ').trim();
  if (clean.length > 55) {
    clean = clean.substring(0, 52).trim() + '...';
  }
  return clean;
}

// Build Pinterest-Native SEO Title (Taste Graph & Guided Search friendly)
function buildPinterestSeoTitle(item) {
  const cat = detectFashionCategory(item.title, item.subcategory);
  const coreName = cleanProductCoreName(item.title);

  let prefix = '';
  let suffix = '';

  switch (cat) {
    case 'saree':
      prefix = 'Festive Saree Styling Inspo';
      suffix = 'Elegant Wedding Guest Look';
      break;
    case 'ethnic':
      prefix = 'Chic Chikankari & Ethnic Inspo';
      suffix = 'Effortless Daily Festive Fit';
      break;
    case 'dress':
      prefix = 'Classy Date Night Dress Inspo';
      suffix = 'Aesthetic Minimalist Lookbook';
      break;
    case 'jeans':
      prefix = 'Aesthetic Denim Outfit Inspo';
      suffix = 'Chic Casual Daily Lookbook';
      break;
    case 'trousers':
      prefix = 'Clean Girl Aesthetic Trousers';
      suffix = 'Office & College Fit Inspo';
      break;
    case 'top':
      prefix = 'Aesthetic Summer Top Inspo';
      suffix = 'Viral Pinterest Outfit Pick';
      break;
    case 'coord':
      prefix = 'Chic Co-ord Set Styling Inspo';
      suffix = 'Effortless Vacation Fit';
      break;
    default:
      prefix = 'Aesthetic Wardrobe Inspo';
      suffix = 'Chic Outfit Recommendation';
  }

  // Format: [Hook] | [Product Name] | [Vibe]
  let title = `${prefix} | ${coreName} - ${suffix}`;
  if (title.length > 95) {
    title = `${prefix} | ${coreName}`;
  }
  if (title.length > 95) {
    title = title.substring(0, 92).trim() + '...';
  }
  return title;
}

// Build Pinterest-Native SEO Description (Recommendation + Styling Guide + Saves Hook)
function buildPinterestSeoDescription(item) {
  const cat = detectFashionCategory(item.title, item.subcategory);
  const cleanTitle = cleanProductCoreName(item.title);
  const price = item.price ? `₹${item.price}` : '';

  let hook = '';
  let stylingTip = '';
  let keywords = '';

  switch (cat) {
    case 'saree':
      hook = `Looking for an ethereal, royal saree look for the upcoming wedding and festive season? Here is an exquisite drape that looks straight out of a designer boutique.`;
      stylingTip = `✨ Styling Guide: Pair with a minimalist contrast blouse, statement jhumkas, delicate dewy makeup, and an elegant potli bag for a royal aesthetic.`;
      keywords = `saree styling ideas, wedding guest outfit inspo, festive wear lookbook, organza saree, traditional elegance, indian wedding style`;
      break;

    case 'ethnic':
      hook = `Effortless grace! This gorgeous ethnic kurti piece combines comfort with timeless heritage craftsmanship, making it an absolute wardrobe staple.`;
      stylingTip = `✨ Styling Guide: Style this with pearl drop earrings, embroidered juttis, and a breezy chiffon dupatta for a graceful day-to-evening transition.`;
      keywords = `chikankari kurti styling, daily ethnic wear inspo, elegant college fits, comfortable festive kurta, indian aesthetic fashion`;
      break;

    case 'dress':
      hook = `The ultimate classy silhouette! If you are searching for an effortless date night or cocktail party outfit that flatters beautifully, this dress is a must-have find.`;
      stylingTip = `✨ Styling Guide: Layer with delicate layered gold necklaces, pointed slingback heels, and a structured mini shoulder bag for an old money chic aesthetic.`;
      keywords = `date night outfit ideas, aesthetic cocktail dress, chic minimalist lookbook, old money aesthetic, party wear inspiration, elegant dresses`;
      break;

    case 'jeans':
      hook = `The flattering denim fit you've been seeing all over Pinterest! Perfect high-waisted cut that elongates the legs and pairs seamlessly with almost anything.`;
      stylingTip = `✨ Styling Guide: Pair with a cropped ribbed knit, retro white sneakers, and an oversized trench or blazer for that effortless street-style look.`;
      keywords = `wide leg jeans outfit, aesthetic denim lookbook, casual college fits, streetwear styling tips, everyday chic fashion, vintage denim inspo`;
      break;

    case 'trousers':
      hook = `The clean-girl aesthetic essential! Tailored to perfection for both professional office wear and chic weekend cafe runs.`;
      stylingTip = `✨ Styling Guide: Tuck in a fitted baby tee or crisp poplin shirt, add minimal chunky loafers, and finish with a sleek belt for a polished Parisian look.`;
      keywords = `clean girl aesthetic, tailored trousers outfit, office wear lookbook, college chic outfit, minimalist style guide, quiet luxury`;
      break;

    case 'top':
      hook = `Obsessed with this aesthetic top! Features an ultra-flattering neckline and premium soft fabric that gives off high-end boutique vibes on a budget.`;
      stylingTip = `✨ Styling Guide: Pair with relaxed high-waist trousers or a pleated mini skirt, dainty rings, and sunglasses for an effortless Pinterest-worthy fit.`;
      keywords = `aesthetic summer tops, outfit inspiration, pinterest viral clothing, cute brunch fits, chic wardrobe essentials, casual styling tips`;
      break;

    default:
      hook = `An effortless aesthetic piece that instantly elevates your everyday wardrobe rotation.`;
      stylingTip = `✨ Styling Guide: Keep accessories minimal and sleek to let the clean silhouette and textures take center stage.`;
      keywords = `aesthetic fashion finds, outfit inspiration, lookbook styling guide, chic wardrobe essentials, trending style`;
  }

  let desc = `💫 ${cleanTitle}\n\n`;
  desc += `${hook}\n\n`;
  desc += `${stylingTip}\n\n`;
  if (price) {
    desc += `🏷️ Curated Pick on TheBhom Deals: Available under ${price} on Amazon India.\n\n`;
  }
  desc += `📌 SAVE this pin to your Outfit Inspiration & Style board so you don't lose it!\n`;
  desc += `Tap through the link to explore full styling details and grab the exact piece.\n\n`;
  desc += `Inspo search tags: ${keywords}`;

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
    const seoTitle = buildPinterestSeoTitle(item);
    const seoDesc = buildPinterestSeoDescription(item);
    const productUrl = `https://thebhom.in/deals/p/${item.slug || item.id}`;
    const hdImg = getHdImageUrl(item.image);
    const guid = `thebhom-pin-${item.id || item.asin || item.slug}`;

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

  // 1. Women's Fashion (Curated for Aesthetic Appeal, Quality & Search Rankings)
  const womenItems = catalog.filter(p => {
    const isWomen = p.department === 'women' ||
           (p.category === 'fashion' && (
             /saree|kurti|dress|jeans|top|suit|anarkali|sharara|ethnic|trouser|women|girl/i.test(p.title) ||
             /women/i.test(p.department || '')
           ));
    const validPrice = p.price >= 149 && p.price <= 9999;
    const hasImage = !!p.image;
    return isWomen && validPrice && hasImage;
  });

  const dedupedWomen = dedupe(womenItems);
  // Sort by rating & discount for highest aesthetic & satisfaction conversion
  dedupedWomen.sort((a, b) => {
    const scoreB = ((b.rating || 4.0) * 10) + ((b.discountNum || 50) * 0.5);
    const scoreA = ((a.rating || 4.0) * 10) + ((a.discountNum || 50) * 0.5);
    return scoreB - scoreA;
  });

  const topWomen = dedupedWomen.slice(0, 250);
  console.log(`Filtered ${womenItems.length} women's items (${dedupedWomen.length} unique). Using top ${topWomen.length} for Pinterest Aesthetic Feed.`);

  const womenXml = generateRssXml({
    title: "Aesthetic Women's Fashion & Outfit Inspo | TheBhom",
    link: "https://thebhom.in/deals/rss-women.xml",
    description: "Curated Indian ethnic wear, sarees, chikankari kurtis, aesthetic dresses, Korean trousers, and daily outfit inspiration lookbooks.",
    items: topWomen
  });

  const womenFeedPath = path.join(FEEDS_DIR, 'pinterest-women-fashion.xml');
  fs.writeFileSync(womenFeedPath, womenXml, 'utf-8');
  fs.writeFileSync(path.join(DEALS_DIR, 'rss-women.xml'), womenXml, 'utf-8');
  console.log(`Saved Pinterest Women's Inspo feed (${(womenXml.length / 1024).toFixed(1)} KB)`);

  // 2. All-Deals Curation Feed
  const allDeals = dedupe(catalog.filter(p => p.price >= 99 && p.price <= 49999 && !!p.image));
  allDeals.sort((a, b) => (b.discountNum || 0) - (a.discountNum || 0));
  const topAll = allDeals.slice(0, 250);

  const allDealsXml = generateRssXml({
    title: "Trending Aesthetic Finds & Style Recommendations | TheBhom",
    link: "https://thebhom.in/deals/rss.xml",
    description: "Curated aesthetic lifestyle finds, fashion lookbooks, and trending recommendations updated daily.",
    items: topAll
  });

  const allDealsFeedPath = path.join(FEEDS_DIR, 'pinterest-all-deals.xml');
  fs.writeFileSync(allDealsFeedPath, allDealsXml, 'utf-8');
  fs.writeFileSync(path.join(DEALS_DIR, 'rss.xml'), allDealsXml, 'utf-8');
  console.log(`Saved Pinterest All Inspo feed (${(allDealsXml.length / 1024).toFixed(1)} KB)`);
}

main().catch(err => {
  console.error('Fatal error generating Pinterest RSS feeds:', err);
  process.exit(1);
});
