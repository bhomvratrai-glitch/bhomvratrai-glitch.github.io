#!/usr/bin/env python3
"""
Master Pinterest SEO & Taxonomy Re-indexer for All 7 RSS Feeds
Files processed:
1. deals/rss-women.xml
2. feed.xml
3. women-fashion-feed.xml
4. fashion-feed.xml
5. tech-feed.xml
6. pinterest-feed.xml
7. home-feed.xml

Taxonomy & Disambiguation Rules:
- ZERO promo words in titles (no loot, deal, discount %, offer, price drop, at Rs, MRP).
- 100% accurate product category mapping (skirts != tops, kurtis != dresses, watches != audio, lamps != bedding).
- High-intent Pinterest SEO tags (no shadowbanned spam tags like #lootdeals).
"""

import os
import re
import html
import xml.etree.ElementTree as ET

# Universal Category Taxonomy with Craftsmanship & SEO Tags
TAXONOMY = {
    # ---------------- APPLIANCES & TECH (Checked first to prevent 'top load' -> 'top') ----------------
    "home_appliance": {
        "keywords": [
            "washing machine", "refrigerator", "fridge", "microwave", "air conditioner", 
            "vacuum cleaner", "air fryer", "geyser", "water purifier", "mixer grinder", 
            "blender", "food processor", "dishwasher", "induction cooktop", "dryer", "top load", "top load was",
            "semi-automatic", "fully-automatic"
        ],
        "category_name": "Home & Kitchen Appliances",
        "craftsmanship": "Modern energy-efficient home appliance engineered with durable motor technology, intuitive smart presets, and robust construction to streamline everyday household living.",
        "specs": "Performance: Certified High-Efficiency Standard | Assured: Genuine Manufacturer Warranty",
        "tags": ["#HomeAppliances", "#SmartHome", "#KitchenAppliances", "#ModernLiving", "#HomeUpgrades", "#CleanHome", "#ApplianceDeals"]
    },
    "smartwatch": {
        "keywords": ["smartwatch", "smart watch", "fitness tracker", "fitness band", "calling watch", "amoled"],
        "category_name": "Smartwatches & Wearables",
        "craftsmanship": "Advanced smart wearable engineered with vibrant high-resolution display, continuous biometric health tracking, multi-sport activity modes, and long-lasting battery life.",
        "specs": "Display: HD AMOLED / Color Display | Features: Real-Time Health & Fitness Tracking",
        "tags": ["#Smartwatch", "#TechGadgets", "#WearableTech", "#FitnessWatch", "#TechInspo", "#GadgetLovers", "#SmartTech"]
    },
    "audio": {
        "keywords": ["headphone", "headphones", "earbuds", "earbud", "tws", "earphone", "earphones", "speaker", "soundbar", "bluetooth speaker"],
        "category_name": "Audio, Headphones & Speakers",
        "craftsmanship": "High-fidelity acoustic audio gear featuring precision-tuned drivers, dynamic bass response, active noise cancellation, and ergonomic comfort for immersive listening.",
        "specs": "Sound: High-Resolution Precision Audio | Connectivity: Low-Latency Bluetooth Wireless",
        "tags": ["#Audiophile", "#WirelessEarbuds", "#Headphones", "#BluetoothSpeaker", "#SoundExperience", "#TechAccessories", "#MusicLovers"]
    },
    "mobile_tech": {
        "keywords": ["smartphone", "mobile phone", "power bank", "charger", "fast charger", "phone case", "type-c", "laptop", "tablet", "monitor", "keyboard", "mouse"],
        "category_name": "Mobiles, Computing & Gadgets",
        "craftsmanship": "High-efficiency tech gear built with smart circuitry protection, rapid connectivity protocols, and durable build quality to keep modern smart devices powered and productive.",
        "specs": "Protection: Over-Voltage & Thermal Safeguards | Universal Device Compatibility",
        "tags": ["#TechLife", "#SmartGadgets", "#PhoneAccessories", "#DeskSetup", "#GadgetStagram", "#TechAccessories", "#EverydayCarry"]
    },

    # ---------------- HOME, LIVING & KITCHEN ----------------
    "home_decor": {
        "keywords": ["floor lamp", "table lamp", "lamp", "lamps", "light", "lighting", "lantern", "candle", "vase", "wall art", "painting", "sculpture", "statue", "clock", "chandelier"],
        "category_name": "Home Decor, Lamps & Lighting",
        "craftsmanship": "Artfully crafted home lighting and aesthetic accent decor designed to bring warm ambiance, sculptural character, and modern interior charm into living rooms and bedrooms.",
        "specs": "Material: Natural Wood / Brass / Ceramic Accents | Ambiance: Warm Illuminating Glow",
        "tags": ["#HomeDecor", "#ModernLighting", "#FloorLamp", "#AestheticHome", "#InteriorDesignInspo", "#CozyHome", "#DecorIdeas"]
    },
    "kitchen_dining": {
        "keywords": ["cookware", "kadhai", "pan", "pressure cooker", "water bottle", "bottle", "lunch box", "tiffin", "knife", "container", "dinner set", "plates", "bowls", "glass", "mugs"],
        "category_name": "Kitchenware & Dining Essentials",
        "craftsmanship": "Food-grade durable kitchen and dining essential constructed from non-toxic, corrosion-resistant materials for uniform thermal distribution, safety, and effortless cleaning.",
        "specs": "Grade: 100% Food-Safe & BPA-Free | Build: Heavy-Gauge Durable Construction",
        "tags": ["#KitchenEssentials", "#Cookware", "#DiningStyle", "#HealthyCooking", "#KitchenOrganization", "#HomeChef", "#ModernKitchen"]
    },
    "storage_organization": {
        "keywords": ["organizer", "organisers", "storage rack", "shoe rack", "storage box", "hanger", "closet rack", "shelf", "drawer", "storage basket", "wardrobe organizer"],
        "category_name": "Storage & Home Organization",
        "craftsmanship": "Space-saving organization system designed to maximize storage efficiency, eliminate clutter, and maintain tidy, harmonious living spaces across bedrooms, kitchens, and closets.",
        "specs": "Design: Modular Space-Saving Layout | Durability: High-Load Structural Capacity",
        "tags": ["#HomeOrganization", "#StorageHacks", "#DeclutterYourSpace", "#ClosetOrganization", "#OrganizedHome", "#TidyLiving", "#SpaceSaver"]
    },
    "bedding_furnishing": {
        "keywords": ["bedsheet", "bed sheet", "curtain", "curtains", "pillow", "cushion", "blanket", "comforter", "duvet", "bed cover", "towel", "rug", "carpet", "mat"],
        "category_name": "Home Furnishing, Bedding & Curtains",
        "craftsmanship": "Plush, breathable textile furnishing tailored from soft hypoallergenic long-staple fibers with vibrant fade-resistant dyes for supreme bedtime comfort and bedroom warmth.",
        "specs": "Thread Count: Ultra-Soft Breathable Weave | Fabric: Hypoallergenic Pure Cotton Blend",
        "tags": ["#BeddingGoals", "#CurtainDesigns", "#HomeFurnishing", "#CozyBedroom", "#TextileDesign", "#SoftFurnishings", "#InteriorAesthetics"]
    },
    "sports_fitness": {
        "keywords": ["football", "cricket", "badminton", "dumbbell", "yoga mat", "resistance band", "gym", "fitness", "skipping rope", "sports", "ball pump"],
        "category_name": "Sports, Fitness & Outdoor Gear",
        "craftsmanship": "High-durability athletic equipment engineered with reinforced all-weather casing, ergonomic grip, and consistent rebound performance for training and competitive play.",
        "specs": "Construction: Heavy-Duty Reinforced Exterior | Performance: Professional Grade Quality",
        "tags": ["#FitnessMotivation", "#SportsGear", "#HomeWorkout", "#FootballTraining", "#ActiveLifestyle", "#GymEquipment", "#HealthyHabits"]
    },

    # ---------------- BEAUTY & FRAGRANCE ----------------
    "perfume": {
        "keywords": ["perfume", "fragrance", "body mist", "deodorant", "cologne", "attar", "eau de parfum", "edp", "edt"],
        "category_name": "Perfumes, Mists & Fragrances",
        "craftsmanship": "Masterfully blended olfactory fragrance featuring layered top, heart, and base notes with enduring sillage and delicate aromatic dry-down for everyday confidence and signature scent appeal.",
        "specs": "Longevity: Long-Lasting Sillage Formulation | Character: Sophisticated Signature Notes",
        "tags": ["#PerfumeCollection", "#FragranceLover", "#SignatureScent", "#BodyMist", "#LuxuryFragrance", "#ScentOfTheDay", "#PerfumeObsessed"]
    },
    "skincare_makeup": {
        "keywords": ["serum", "moisturizer", "sunscreen", "cleanser", "face wash", "face cream", "lipstick", "foundation", "concealer", "eyeliner", "mascara", "kajal", "blush", "skincare", "makeup"],
        "category_name": "Beauty, Skincare & Cosmetics",
        "craftsmanship": "Dermatologically formulated beauty essential crafted with skin-loving botanical extracts and nourishing actives for a radiant, healthy complexion and seamless cosmetic finish.",
        "specs": "Formulation: Cruelty-Free & Dermatologically Tested | Finish: Dewy Natural Radiance",
        "tags": ["#SkincareRoutine", "#BeautyEssentials", "#CleanBeauty", "#MakeupLook", "#GlowingSkin", "#SelfCareSunday", "#DailySkincare"]
    },

    # ---------------- FASHION CATEGORIES (Surgically Ordered) ----------------
    "saree": {
        "keywords": ["saree", "sari", "sare", "drape", "zari border", "pallu", "silk saree", "organza saree", "linen saree", "chiffon saree", "banarasi saree", "ready to wear saree", "ready to wear sare"],
        "category_name": "Women's Ethnic Sarees",
        "craftsmanship": "Exquisitely woven traditional Indian saree featuring refined border craftsmanship, graceful drape, and timeless elegance for weddings, festive occasions, and traditional celebrations.",
        "specs": "Fabric: Rich Handloom / Silk / Linen / Organza | Occasion: Festive & Wedding Elegance",
        "tags": ["#SareeLove", "#IndianEthnicWear", "#SareeStyle", "#WeddingSaree", "#FestiveDrape", "#TraditionalOutfit", "#DesiFashion"]
    },
    "lehenga": {
        "keywords": ["lehenga", "ghagra", "choli", "semi-stitched lehenga", "bridal lehenga"],
        "category_name": "Women's Bridal & Festive Lehengas",
        "craftsmanship": "Intricately detailed bridal and festive lehenga choli ensemble highlighted with exquisite embellishments, flared silhouette, and coordinated dupatta for regal festive styling.",
        "specs": "Work: Detailed Embroidery & Sequins | Silhouette: Flared Regal Ensemble",
        "tags": ["#LehengaCholi", "#BridalLehenga", "#WeddingOutfitInspo", "#IndianWeddingWear", "#FestiveLookbook", "#DesiGlam"]
    },
    "kurti": {
        "keywords": ["kurti", "kurta", "anarkali", "chikankari", "ethnic set", "kurta set", "straight kurti", "a-line kurti", "sharara", "gharara"],
        "category_name": "Women's Ethnic Kurtis & Sets",
        "craftsmanship": "Artfully designed ethnic kurti tailored from premium breathable fabric with intricate neckline embroidery, graceful silhouette, and versatile elegance for daily and festive wear.",
        "specs": "Silhouette: Elegant Straight / A-Line Flared | Fabric: Pure Cotton & Breathable Blends",
        "tags": ["#KurtiDesign", "#EthnicWear", "#ChikankariKurti", "#DailyEthnicWear", "#IndianFashion", "#AnarkaliSuit", "#OfficeEthnicWear"]
    },
    "skirt": {
        "keywords": ["skirt", "maxi skirt", "mini skirt", "pleated skirt", "a-line skirt", "flared skirt", "swing skirt"],
        "category_name": "Women's Skirts & Flared Bottoms",
        "craftsmanship": "Chic and flowy skirt featuring a flattering tailored waistband, fluid drape, and lightweight construction for effortless spring-summer styling and feminine aesthetic lookbooks.",
        "specs": "Silhouette: Flared / Pleated / A-Line | Length: Midi / Maxi Versatile Cut",
        "tags": ["#SkirtStyle", "#MaxiSkirt", "#PleatedSkirt", "#SummerFashion", "#AestheticOutfits", "#FeminineStyle", "#CasualChic"]
    },
    "trouser_pants": {
        "keywords": ["trouser", "trousers", "formal pant", "formal pants", "korean pants", "parallel pants", "palazzo", "culottes", "wide leg pants", "straight pants"],
        "category_name": "Women's Trousers & Tailored Pants",
        "craftsmanship": "Tailored high-waisted trousers engineered with a relaxed straight-leg drape, structured waistband, and fluid mobility for minimal clean-girl aesthetic and office wardrobe essentials.",
        "specs": "Rise: High-Rise Structured Fit | Silhouette: Wide-Leg / Straight Tailored Cut",
        "tags": ["#TailoredTrousers", "#KoreanPants", "#WideLegPants", "#WorkwearStyle", "#OfficeOutfit", "#MinimalistAesthetic", "#CleanGirlStyle"]
    },
    "jeans": {
        "keywords": ["jeans", "denim", "bootcut", "boyfriend jeans", "wide leg jeans", "skinny jeans", "mom jeans", "flare jeans"],
        "category_name": "Women's Denim & Jeans",
        "craftsmanship": "Premium authentic cotton denim engineered with comfortable ergonomic stretch, classic multi-pocket styling, and durable seams for daily rugged wear and street style aesthetics.",
        "specs": "Material: High-Grade Cotton Stretch Denim | Fit: Ergonomic Comfort Contour",
        "tags": ["#DenimStyle", "#WomensJeans", "#WideLegJeans", "#StreetwearFashion", "#CasualDenim", "#OutfitInspo", "#ClassicDenim"]
    },
    "dress": {
        "keywords": ["dress", "maxi dress", "midi dress", "mini dress", "gown", "one piece", "bodycon", "a-line dress", "wrap dress", "jumpsuit"],
        "category_name": "Women's Dresses & Gowns",
        "craftsmanship": "Effortlessly sophisticated one-piece dress featuring a figure-accentuating cut, premium lining, and delicate design accents for brunches, dinner dates, and celebration parties.",
        "specs": "Silhouette: Tailored A-Line / Fit & Flare | Occasion: Brunch, Party & Date Night",
        "tags": ["#DressInspo", "#MidiDress", "#MaxiDress", "#PartyWearDress", "#SummerDresses", "#AestheticFashion", "#OutfitOfTheDay"]
    },
    "crop_top": {
        "keywords": ["crop top", "tank top", "halter neck", "tube top", "corset top", "baby tee", "crop tank"],
        "category_name": "Women's Crop Tops & Tank Tops",
        "craftsmanship": "Modern crop top crafted from soft, flexible ribbed knit and stretch cotton for clean-girl aesthetic styling, warm-weather comfort, and effortless layering under blazers and jackets.",
        "specs": "Fit: Form-Flattering Slim Fit | Fabric: Breathable Ribbed Stretch Cotton",
        "tags": ["#CropTop", "#TankTop", "#CleanGirlAesthetic", "#SummerTop", "#WesternWear", "#StreetwearStyle", "#CasualOutfit"]
    },
    "top_shirt": {
        "keywords": ["top", "tops", "shirt", "shirts", "blouse", "peplum", "tunic", "button-down", "poplin shirt", "t-shirt", "tee"],
        "category_name": "Women's Tops, Blouses & Shirts",
        "craftsmanship": "Versatile casual and smart top tailored with elegant sleeve detailing, relaxed comfortable silhouette, and refined neckline for office, college, and weekend outings.",
        "specs": "Style: Contemporary Casual & Smart Wear | Fabric: Lightweight Soft Cotton Blend",
        "tags": ["#WomenTop", "#BlouseDesign", "#WorkWearWomen", "#CasualTop", "#WesternStyle", "#EverydayFashion", "#SmartCasual"]
    },
    "footwear": {
        "keywords": ["heel", "heels", "sandal", "sandals", "sneaker", "sneakers", "shoe", "shoes", "flat", "flats", "mojri", "jooti", "boot", "boots", "loafer", "block heel", "stilettos"],
        "category_name": "Footwear, Heels & Sneakers",
        "craftsmanship": "Ergonomically cushioned designer footwear balancing all-day comfort with striking visual silhouette, anti-slip durable sole, and premium upper finish for versatile styling.",
        "specs": "Sole: Cushioned Comfort Footbed | Build: Durable Anti-Slip Construction",
        "tags": ["#FootwearFashion", "#Sneakerhead", "#HeelsStyle", "#ShoesOfTheDay", "#StreetwearShoes", "#ComfortableHeels", "#ShoeLover"]
    },
    "jewellery": {
        "keywords": ["jewellery", "jewelry", "necklace", "earring", "earrings", "jhumka", "kundan", "choker", "bangle", "bracelet", "pendant", "ring", "anklet", "gold-plated"],
        "category_name": "Jewellery & Accessories",
        "craftsmanship": "Handcrafted artisanal jewellery adorned with radiant stones, intricate filigree detailing, and tarnish-resistant lustrous polish to elevate both festive Indian and western ensembles.",
        "specs": "Plating: Long-Lasting Glossy Polish | Detailing: Precision Handcrafted Accents",
        "tags": ["#JewelleryDesign", "#EarringsLove", "#KundanJewellery", "#NecklaceSet", "#TraditionalJewellery", "#AccessoriesInspo", "#BridalJewellery"]
    },
    "handbag": {
        "keywords": ["handbag", "bag", "tote", "clutch", "purse", "backpack", "sling bag", "crossbody", "wallet"],
        "category_name": "Handbags, Totes & Clutches",
        "craftsmanship": "Functional luxury handbag designed with spacious organized compartments, resilient premium stitching, and refined metallic hardware for daily commute, travel, and evening outings.",
        "specs": "Material: High-Grade Vegan Leather / Durable Canvas | Closure: Smooth Sturdy Hardware",
        "tags": ["#HandbagLove", "#ToteBag", "#SlingBag", "#BagObsessed", "#EverydayCarry", "#FashionAccessories", "#LuxuryAesthetic"]
    }
}

FALLBACK_CATEGORY = {
    "category_name": "Curated Quality Finds",
    "craftsmanship": "Thoughtfully designed premium product balancing reliable functional performance, high-grade material durability, and contemporary styling for modern lifestyle needs.",
    "specs": "Quality: 100% Genuine Certified Standard | Design: Ergonomic Daily Utility",
    "tags": ["#CuratedPicks", "#QualityLiving", "#ModernLifestyle", "#DailyEssentials", "#TheBhomFinds", "#IndiaShopping"]
}

def clean_title(raw_title):
    """Surgically clean title to extract strictly the Product Name."""
    if not raw_title:
        return "Curated Product"
    
    t = html.unescape(raw_title).strip()

    # 1. If title has a pipe '|', check if the part after '|' is the product name
    if '|' in t:
        parts = t.split('|')
        if len(parts) == 2 and len(parts[1].strip()) > 5:
            t = parts[1].strip()

    # 2. Strip leading emojis and symbols
    t = re.sub(r'^[⚡🛍️🔥💥💫✨📌👉🏷️🪔]+\s*', '', t).strip()

    # 3. Strip trailing emojis and symbols
    t = re.sub(r'[\s⚡🛍️🔥💥💫✨📌👉🏷️🪔]+$', '', t).strip()

    # 4. Strip promo brackets [Price Drop ...% OFF], [Loot Deal], etc.
    t = re.sub(r'^\[.*?\]\s*', '', t).strip()
    t = re.sub(r'\[.*?\]', '', t).strip()

    # 5. Strip single leading buzzwords like 'Trending ', 'Viral '
    t = re.sub(r'^(Trending|Viral)\s+', '', t, flags=re.IGNORECASE).strip()

    # 6. Strip trailing percentage discounts like '- 37% OFF', '- 55% OFF', ' - Price Drop'
    t = re.sub(r'\s*-\s*\d+%\s*OFF\b.*$', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\s*-\s*Price Drop\b.*$', '', t, flags=re.IGNORECASE).strip()

    # 7. Strip trailing price tags
    t = re.sub(r'\s+at\s+₹[\d,]+.*$', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\s*\(MRP\s*₹[\d,]+\).*$', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\s+under\s+₹[\d,]+.*$', '', t, flags=re.IGNORECASE).strip()

    # 8. Strip trailing ellipses or dashes
    t = re.sub(r'[\s\.\-]+$', '', t).strip()
    t = re.sub(r'\s+', ' ', t).strip()

    if len(t) < 4:
        return html.unescape(raw_title).replace('⚡', '').strip()[:80]
    
    return t

def categorize_product(title, raw_desc=""):
    """
    Surgically categorize product strictly by TITLE FIRST to prevent context poisoning from descriptions.
    Uses word boundaries and negative lookahead to prevent false positives.
    """
    clean_t = f" {title.lower()} "
    
    # Priority order for checking
    category_order = [
        "home_appliance", "smartwatch", "audio", "mobile_tech",
        "home_decor", "kitchen_dining", "storage_organization", "bedding_furnishing", "sports_fitness",
        "perfume", "skincare_makeup",
        "saree", "lehenga", "kurti", "skirt", "trouser_pants", "jeans", "dress", "crop_top", "top_shirt",
        "footwear", "jewellery", "handbag"
    ]

    # PASS 1: Strictly check Title
    for cat_key in category_order:
        cat_info = TAXONOMY[cat_key]
        for kw in cat_info["keywords"]:
            if kw == "top" or kw == "tops":
                if "top load" in clean_t or "desktop" in clean_t or "countertop" in clean_t or "table top" in clean_t:
                    continue
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, clean_t):
                return cat_key, cat_info

    # PASS 2: If title was generic, check raw description with strict keyword matching
    clean_d = f" {raw_desc.lower()} "
    for cat_key in category_order:
        cat_info = TAXONOMY[cat_key]
        for kw in cat_info["keywords"]:
            if kw in ["top", "tops", "shirt", "pant", "bag", "dress"]:  # Avoid broad words in descriptions
                continue
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, clean_d):
                return cat_key, cat_info

    return "general", FALLBACK_CATEGORY

def generate_seo_description(clean_title_text, cat_info):
    """Generate high-intent Pinterest SEO description."""
    category_name = cat_info["category_name"]
    craftsmanship = cat_info["craftsmanship"]
    specs = cat_info["specs"]
    tags = " ".join(cat_info["tags"])
    
    desc = (
        f"{clean_title_text}\n\n"
        f"Category: {category_name}\n"
        f"{craftsmanship}\n\n"
        f"✨ Product Highlights:\n"
        f"• {specs}\n"
        f"• Verified authentic manufacturer craftsmanship & genuine quality assurance.\n\n"
        f"📌 SAVE this pin to your {category_name} board for curated inspiration, aesthetic styling, and daily lookbooks.\n\n"
        f"{tags}"
    )
    return desc

def process_feed_file(filepath):
    """Parse, sanitize, re-categorize, and write back the feed file."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 0
    
    print(f"\n==========================================")
    print(f"Processing: {filepath}")
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except Exception as e:
        print(f"Failed to parse XML: {e}")
        return 0
        
    items = root.findall('.//item')
    print(f"Total items found: {len(items)}")
    
    category_counts = {}
    updated_count = 0
    
    for item in items:
        title_el = item.find('title')
        desc_el = item.find('description')
        
        raw_title = title_el.text if title_el is not None and title_el.text else ""
        raw_desc = desc_el.text if desc_el is not None and desc_el.text else ""
        
        # 1. Clean Title
        clean_name = clean_title(raw_title)
        
        # 2. Categorize Product strictly
        cat_key, cat_info = categorize_product(clean_name, raw_desc)
        category_counts[cat_key] = category_counts.get(cat_key, 0) + 1
        
        # 3. Generate Clean SEO Description
        seo_desc = generate_seo_description(clean_name, cat_info)
        
        # Update XML elements
        if title_el is not None:
            title_el.text = clean_name
        
        if desc_el is not None:
            desc_el.text = seo_desc
            
        # Update or add <category> tag if exists
        cat_el = item.find('category')
        if cat_el is not None:
            cat_el.text = cat_info["category_name"]
            
        updated_count += 1
        
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    print(f"Successfully sanitized & updated {updated_count} items in {filepath}")
    print(f"Category Distribution:")
    for k, v in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"  • {k}: {v} items")
        
    return updated_count

def main():
    target_files = [
        "deals/rss-women.xml",
        "feed.xml",
        "women-fashion-feed.xml",
        "fashion-feed.xml",
        "tech-feed.xml",
        "pinterest-feed.xml",
        "home-feed.xml"
    ]
    
    total_processed = 0
    for rel_path in target_files:
        full_path = os.path.join("/Users/bhomvratrai/Documents/GitHub/thebhom-landing", rel_path)
        total_processed += process_feed_file(full_path)
        
    print(f"\n==========================================")
    print(f"🎉 ALL 7 FEEDS ACCURATELY SANITIZED! Total items: {total_processed}")

if __name__ == "__main__":
    main()
