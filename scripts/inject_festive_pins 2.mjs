import fs from 'fs';
import path from 'path';

const REPO_DIR = '/Users/bhomvratrai/Documents/GitHub/thebhom-landing';
const STOREFRONT_URL = 'https://www.amazon.in/shop/bhom120704';

const FESTIVE_ITEMS = [
  {
    guid: 'thebhom-festive-pin-1-karwachauth-anarkali',
    title: 'Trending Red Anarkali Kurti Set For Karwa Chauth & Diwali 🪔✨',
    link: STOREFRONT_URL,
    image: 'https://thebhom.in/assets/festive/festive_pin_1.jpg',
    description: `Royal Crimson Red Embroidered Anarkali Kurti Set with Zari gold border & dupatta lookbook for Karwa Chauth, Diwali Pooja & Festive Parties.

✨ FESTIVE OUTFIT HIGHLIGHTS:
• Silhouette: Flared Floor-Length Anarkali with intricate Zari neckline
• Fabric: Rich Silk Blend with lightweight embroidered organza dupatta
• Styling: Pair with Kundan jhumkas and traditional golden mojris
• Occasion: Karwa Chauth Sargi & Evening Pooja, Diwali Family Gatherings

👉 TAP TO EXPLORE COMPLETE FESTIVE LOOKBOOK & VERIFIED FINDS ON AMAZON STOREFRONT:
amazon.in/shop/bhom120704

#diwalilook #karwachauthoutfit #anarkalisuit #redkurti #festivewear #indianethnicwear #amazonfashion`
  },
  {
    guid: 'thebhom-festive-pin-2-tissue-silk-saree',
    title: 'Viral Golden Tissue Silk Saree Lookbook for Diwali Pooja ✨🪔',
    link: STOREFRONT_URL,
    image: 'https://thebhom.in/assets/festive/festive_pin_2.jpg',
    description: `Aesthetic Golden Beige Tissue Silk Saree paired with contrast festive green embroidered blouse styling for Diwali night & wedding guests.

✨ SAREE HIGHLIGHTS:
• Fabric: Premium shimmering Tissue Silk with scalloped Zari border
• Blouse: Contrast Emerald Green handcrafted zardozi embroidery
• Draping: Light, crisp structure that holds pleats effortlessly
• Look: Regal modern royal look for Diwali lights and card parties

👉 TAP TO EXPLORE DIRECT VERIFIED OUTFIT PICKS ON OUR STOREFRONT:
amazon.in/shop/bhom120704

#diwalisaree #tissuesaree #festivesaree #ethniclookbook #sareelover #festivefashion #indianwedding`
  },
  {
    guid: 'thebhom-festive-pin-3-pastel-organza-kurti',
    title: 'Chic Pastel Organza Floral Kurti Set Lookbook 🌸✨',
    link: STOREFRONT_URL,
    image: 'https://thebhom.in/assets/festive/festive_pin_3.jpg',
    description: `Aesthetic Pastel Blush Pink Floral Embroidered Organza Kurti Pant Set with light dupatta for daytime Diwali gatherings & festive brunches.

✨ OUTFIT HIGHLIGHTS:
• Material: Semi-sheer Organza with delicate floral threadwork
• Fit: Straight comfort-cut kurti with matching cropped trousers
• Vibe: Soft girl aesthetic meets traditional Indian festive wear
• Accessories: Pearl choker necklace and minimal block heels

👉 TAP TO EXPLORE VERIFIED PICKS ON OUR STOREFRONT:
amazon.in/shop/bhom120704

#organzakurti #diwalioutfit #pastelfashion #festivelook #kurtiset #ethnicwear #softgirlaesthetic`
  },
  {
    guid: 'thebhom-festive-pin-4-navy-velvet-kurti',
    title: 'Trending Royal Blue Velvet Festive Kurti Set Styling 🪔💙',
    link: STOREFRONT_URL,
    image: 'https://thebhom.in/assets/festive/festive_pin_4.jpg',
    description: `Rich Royal Navy Blue Velvet Embroidered Straight Kurti with Mustard Gold Zari border dupatta lookbook for winter weddings & Diwali nights.

✨ VELVET SUIT HIGHLIGHTS:
• Texture: Heavy plush micro-velvet with antique gold neck yoke
• Dupatta: Rich woven Banarasi silk in mustard gold
• Season: Perfect for November-December cool evening celebrations & Bhai Dooj
• Silhouette: Regal straight cut with wide palazzos

👉 TAP FOR DIRECT VERIFIED COLLECTION ON OUR STOREFRONT:
amazon.in/shop/bhom120704

#velvetkurti #winterfestive #diwalifashion #ethnicchic #indianoutfits #bhaidooj`
  },
  {
    guid: 'thebhom-festive-pin-5-wine-georgette-suit',
    title: 'Aesthetic Wine Festive Suit Set Under ₹799 - Diwali Lookbook 🍷✨',
    link: STOREFRONT_URL,
    image: 'https://thebhom.in/assets/festive/festive_pin_5.jpg',
    description: `Deep Wine Plum Georgette Festive Kurti Palazzo Set with Gotta Patti details for Karwa Chauth evening and Diwali gatherings.

✨ BUDGET FESTIVE HIGHLIGHTS:
• Work: Classic Rajasthani Gota Patti neck yoke & border
• Fabric: Breathable faux Georgette with inner lining
• Price Sweet Spot: Under ₹799 verified festive budget find
• Comfort: Lightweight flare palazzo for comfortable all-day wear

👉 TAP FOR VERIFIED DIRECT PICKS ON OUR STOREFRONT:
amazon.in/shop/bhom120704

#budgetdiwali #festivekurti #gotapatti #karwachauthlook #amazonfashion #ethnicwear #amazonfinds`
  }
];

function escapeXml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function generateItemXml(item) {
  return `    <item>
      <title>${escapeXml(item.title)}</title>
      <link>${escapeXml(item.link)}</link>
      <description>${escapeXml(item.description)}</description>
      <enclosure url="${escapeXml(item.image)}" type="image/jpeg" length="850000" />
      <guid isPermaLink="false">${escapeXml(item.guid)}</guid>
      <pubDate>Fri, 09 Oct 2026 17:35:00 GMT</pubDate>
    </item>`;
}

function updateFeed(filePath) {
  if (!fs.existsSync(filePath)) {
    console.warn(`File not found: ${filePath}`);
    return;
  }
  let content = fs.readFileSync(filePath, 'utf-8');
  
  // Clean existing copies of these guids if present
  for (const item of FESTIVE_ITEMS) {
    const guidRegex = new RegExp(`<item>[\\s\\S]*?<guid[^>]*>${item.guid}<\\/guid>[\\s\\S]*?<\\/item>`, 'g');
    content = content.replace(guidRegex, '');
  }

  const itemsXml = FESTIVE_ITEMS.map(generateItemXml).join('\n');
  const insertMarker = '<atom:link href="';
  const markerIdx = content.indexOf(insertMarker);
  
  if (markerIdx !== -1) {
    const endOfTag = content.indexOf('/>', markerIdx) + 2;
    content = content.slice(0, endOfTag) + '\n' + itemsXml + content.slice(endOfTag);
    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`✅ Successfully injected 5 Festive Pins into: ${filePath}`);
  } else {
    console.error(`Marker not found in ${filePath}`);
  }
}

updateFeed(path.join(REPO_DIR, 'women-fashion-feed.xml'));
updateFeed(path.join(REPO_DIR, 'pinterest-feed.xml'));
updateFeed(path.join(REPO_DIR, 'fashion-feed.xml'));
console.log('🎉 Done updating all Pinterest RSS feeds with 5 Festive High-Traffic Pins!');
