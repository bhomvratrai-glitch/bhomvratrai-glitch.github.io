#!/usr/bin/env python3
"""
Re-indexes and sanitizes all Pinterest RSS feeds (pinterest-feed.xml & women-fashion-feed.xml):
1. Clean Titles: Removes ALL promo/spam words (Loot, Deal, % OFF, Discounts, Today Only, Save, etc.).
   Leaves ONLY pure, natural product names for high-intent Pinterest search matching.
2. Precise Categorization (26+ Fashion & Beauty Categories):
   Eliminates wrong categorization (e.g. skirts categorized as ethnic tops, or makeup labeled with fabric).
3. Native SEO Descriptions & Tags:
   Category-accurate craftsmanship (fabric for clothes, kundan/plating for jewellery, soles for footwear,
   pigment/formula for cosmetics) and 100% relevant Pinterest search hashtags.
4. Purges corrupt/placeholder entries (brand-only titles, promo scraps, duplicates).
"""

import os
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PINTEREST_FEED = os.path.join(BASE_DIR, "pinterest-feed.xml")
WOMEN_FEED = os.path.join(BASE_DIR, "women-fashion-feed.xml")

TAXONOMY = [
    {
        "id": "saree",
        "name": "Designer Saree",
        "keywords": ["saree", "sari", "kanjivaram", "banarasi", "chanderi", "silk drape", "georgette saree", "chiffon saree", "organza saree", "bandhani", "paithani", "patola", "6-yard", "poshak", "drape"],
        "occasion": "festivals, wedding ceremonies, family celebrations, and formal traditional gatherings",
        "craftsmanship": "Crafted with rich fabric drape, intricate borders, and traditional artisanal detailing",
        "styling": "Pair with a contrasting designer blouse, traditional jhumkas, and embellished mojaris or heels.",
        "hashtags": "#SareeLove #IndianSaree #DesignerSaree #SareeCollection #EthnicSaree #FestiveSaree #TraditionalWear"
    },
    {
        "id": "kurti",
        "name": "Kurti & Kurta Set",
        "keywords": ["kurti", "kurta", "kurta set", "kurti set", "chikankari", "anarkali suit", "angrakha", "straight kurta", "a-line kurti", "suit set", "salwar", "churidar", "tunic"],
        "occasion": "everyday office wear, college, festive gatherings, and casual day outings",
        "craftsmanship": "Crafted with breathable soft fabric, delicate embroidery or block prints, and refined neckline stitching",
        "styling": "Pair with matching palazzos, cigarette pants, or leggings, and oxidized silver jhumkis.",
        "hashtags": "#KurtiDesign #KurtaSet #IndianKurti #DailyEthnic #CottonKurti #EthnicWearForWomen #FestiveKurti"
    },
    {
        "id": "lehenga",
        "name": "Lehenga Choli",
        "keywords": ["lehenga", "choli", "ghagra", "chaniya choli", "reception sangeet", "sangeet look", "bridal wear", "bridal semi-stitched", "garba", "navratri"],
        "occasion": "weddings, sangeet ceremonies, grand festive parties, and reception nights",
        "craftsmanship": "Features an ornate flared silhouette, intricate zardozi or mirror work, and a matching sheer dupatta",
        "styling": "Style with a heavy kundan choker set, statement maang tikka, and regal high heels.",
        "hashtags": "#LehengaCholi #BridalLehenga #WeddingOutfit #DesignerLehenga #FestiveLehenga #IndianWeddingFashion"
    },
    {
        "id": "anarkali",
        "name": "Anarkali Gown",
        "keywords": ["anarkali", "ethnic gown", "floor length gown", "party gown", "maxi gown"],
        "occasion": "family celebrations, evening cocktail events, and traditional pujas",
        "craftsmanship": "Tailored with a sweeping flared hemline, graceful pleats, and elegant yoke embroidery",
        "styling": "Pair with dangling chandelier earrings, dewy evening makeup, and metallic block heels.",
        "hashtags": "#AnarkaliSuit #IndianGown #EthnicGown #FestiveFashion #AnarkaliDress #TraditionalGown"
    },
    {
        "id": "skirt",
        "name": "Women's Skirt",
        "keywords": ["skirt", "midaxi skirt", "pleated skirt", "mini skirt", "maxi skirt", "pencil skirt", "a-line skirt", "wrap skirt"],
        "occasion": "casual brunches, weekend getaways, college styling, and modern street style",
        "craftsmanship": "Tailored with fluid pleats, a comfortable waistband, and premium drape",
        "styling": "Pair with a tucked-in shirt, a fitted crop top, or a knit sweater with ankle boots or sneakers.",
        "hashtags": "#WomensSkirt #MidiSkirt #PleatedSkirt #MaxiSkirt #WesternOutfit #CasualStyle #StreetStyleWomen"
    },
    {
        "id": "western_dress",
        "name": "Women's Western Dress",
        "keywords": ["dress", "midi dress", "maxi dress", "mini dress", "bodycon", "shift dress", "wrap dress", "sheath dress", "slip dress", "a-line dress", "halter dress", "fit and flare dress", "sundress"],
        "occasion": "casual brunches, weekend vacations, dinner dates, and evening parties",
        "craftsmanship": "Crafted with lightweight comfortable fabric, a flattering modern cut, and flawless finishing",
        "styling": "Pair with classic strap heels or sneakers, a minimalist tote bag, and delicate layered chains.",
        "hashtags": "#WomensDress #WesternDress #MaxiDress #MidiDress #SummerDress #PartyWearDress #OOTDDress"
    },
    {
        "id": "jumpsuit",
        "name": "Women's Jumpsuit & Romper",
        "keywords": ["jumpsuit", "romper", "playsuit", "dungaree"],
        "occasion": "stylish weekend outings, dinner parties, airport looks, and semi-formal events",
        "craftsmanship": "Designed with a tailored waistline, comfortable modern silhouette, and breathable fabric",
        "styling": "Style with block heels, a structured handbag, and statement hoop earrings.",
        "hashtags": "#WomensJumpsuit #RomperStyle #ChicOutfit #OnePieceOutfit #SmartCasual #ModernFashion"
    },
    {
        "id": "coord_set",
        "name": "Women's Co-ord Set",
        "keywords": ["co-ord", "coord", "two piece set", "two-piece", "matching set", "three-piece", "3-piece set"],
        "occasion": "travel, vacation resort wear, casual outings, and trendy airport looks",
        "craftsmanship": "Crafted with perfectly coordinated prints, premium breathable fabric, and a relaxed stylish fit",
        "styling": "Pair with minimal slides, oversized sunglasses, and a crossbody sling bag.",
        "hashtags": "#CoordSet #MatchingSet #TwoPieceSet #VacationOutfit #ResortWear #AirportLook"
    },
    {
        "id": "top",
        "name": "Women's Top & T-Shirt",
        "keywords": ["top", "crop top", "peplum", "corset", "tank top", "tee", "t-shirt", "halter neck", "sleeveless top", "camisole", "halter"],
        "occasion": "workdays, college presentations, casual meetups, and travel days",
        "craftsmanship": "Crafted with ultra-soft breathable fabric, a contemporary neckline, and comfortable fit",
        "styling": "Pair with high-waist jeans, tailored trousers, or a pleated midi skirt.",
        "hashtags": "#WomensTop #CropTop #CasualTop #SummerTop #KoreanFashion #StreetStyleTops #EverydayChic"
    },
    {
        "id": "shirt",
        "name": "Women's Shirt & Blouse",
        "keywords": ["shirt", "button down", "blouse", "collared", "linen shirt", "oversized shirt"],
        "occasion": "office meetings, formal presentations, smart casual Fridays, and coffee runs",
        "craftsmanship": "Tailored with a crisp collar, neat button placket, and smooth lightweight cotton or linen blend",
        "styling": "Style with high-waisted parallel trousers, a sleek leather belt, and loafers or pointed pumps.",
        "hashtags": "#WomensShirt #OfficeWear #FormalShirt #ClassicStyle #WorkwearStyle #SmartCasualWomen"
    },
    {
        "id": "trouser",
        "name": "Women's Trousers & Pants",
        "keywords": ["trouser", "pant", "palazzo", "culotte", "chino", "cargo", "flare pant", "yoga pant", "legging", "jegging", "tight"],
        "occasion": "office formals, meetings, casual brunches, and versatile everyday styling",
        "craftsmanship": "Designed with a tailored waistband, smooth straight-leg silhouette, and convenient pockets",
        "styling": "Pair with a crisp tucked-in shirt, a fitted crop top, or a short ethnic kurti.",
        "hashtags": "#WomenPants #TrousersForWomen #PalazzoPants #OfficePants #SmartCasual #FormalPants"
    },
    {
        "id": "jeans",
        "name": "Women's Jeans & Denim",
        "keywords": ["jeans", "denim", "wide leg", "mom jean", "skinny jean", "flared jean", "bootcut jean"],
        "occasion": "casual day-outs, college, road trips, and relaxed weekend styling",
        "craftsmanship": "Crafted with durable stretch denim fabric, high-rise support, and reinforced stitching",
        "styling": "Pair with an oversized graphic tee, a tailored blazer, or a chic crop top with white sneakers.",
        "hashtags": "#WomensJeans #DenimStyle #HighWaistJeans #WideLegJeans #CasualDenim #EverydayDenim"
    },
    {
        "id": "shorts",
        "name": "Women's Shorts",
        "keywords": ["short", "bermuda", "denim short", "hot pant"],
        "occasion": "summer vacations, beach trips, casual workouts, and relaxed loungewear",
        "craftsmanship": "Crafted with lightweight breathable fabric and a flexible comfortable waistband",
        "styling": "Pair with a loose linen shirt, slides or white sneakers, and UV sunglasses.",
        "hashtags": "#WomensShorts #SummerShorts #CasualShorts #DenimShorts #VacationStyle #SummerOutfit"
    },
    {
        "id": "jacket",
        "name": "Women's Jacket & Blazer",
        "keywords": ["jacket", "blazer", "coat", "shrug", "bomber", "trench", "quilted jacket", "waistcoat"],
        "occasion": "office presentations, layered autumn outings, evening events, and travel",
        "craftsmanship": "Tailored with structured shoulders, smooth inner lining, and premium outer fabric",
        "styling": "Layer over a basic tee and jeans, or wear over a formal sheath dress for a powerful look.",
        "hashtags": "#WomensBlazer #JacketsForWomen #Outerwear #LayeringStyle #PowerDressing #OfficeChic"
    },
    {
        "id": "sweater",
        "name": "Women's Sweater & Knitwear",
        "keywords": ["sweater", "cardigan", "pullover", "sweatshirt", "hoodie", "winterwear", "knitwear", "knit"],
        "occasion": "cozy winter days, chilly evenings, college, and casual travel",
        "craftsmanship": "Knitted with soft insulating yarn for maximum warmth, comfort, and snug stretch",
        "styling": "Pair with fleece-lined leggings, straight jeans, and ankle boots or warm sneakers.",
        "hashtags": "#WomensSweater #Knitwear #Cardigan #WinterFashion #CozyStyle #SweaterWeather"
    },
    {
        "id": "heels",
        "name": "Women's Heels & Pumps",
        "keywords": ["heel", "stiletto", "pump", "wedge", "block heel", "kitten heel"],
        "occasion": "weddings, cocktail parties, festive functions, and formal corporate events",
        "craftsmanship": "Crafted with a cushioned footbed, ergonomic heel balancing, and anti-skid durable sole",
        "styling": "Pair with flowy ethnic sarees, lehengas, or sleek evening gowns for an elevated silhouette.",
        "hashtags": "#WomensHeels #BlockHeels #PartyHeels #Stilettos #FashionFootwear #HeelsLove"
    },
    {
        "id": "flats",
        "name": "Women's Flats & Sandals",
        "keywords": ["sandal", "flat", "slide", "mojari", "kolhapuri", "jutti", "mule", "flip flop", "slippers"],
        "occasion": "festive celebrations, daily commute, casual walks, and ethnic gatherings",
        "craftsmanship": "Features handcrafted detailing, soft padded insole, and flexible non-slip base",
        "styling": "Complements anarkalis, kurtas, or breezy summer dresses with effortless comfort.",
        "hashtags": "#WomensFlats #ComfortSandals #EthnicJutti #Kolhapuri #DailyFootwear #SummerSandals"
    },
    {
        "id": "sneakers",
        "name": "Women's Sneakers & Shoes",
        "keywords": ["sneaker", "shoes", "shoe", "boot", "loafer", "running shoes", "trainer"],
        "occasion": "daily college, travel, fitness walks, and trendy street fashion",
        "craftsmanship": "Constructed with breathable mesh or durable vegan leather with high-traction rubber soles",
        "styling": "Pair with high-waist jeans, joggers, shorts, or even flowy midi dresses for an athleisure vibe.",
        "hashtags": "#WomensSneakers #CasualShoes #StreetwearShoes #ComfortShoes #Athleisure #SneakerStyle"
    },
    {
        "id": "bags",
        "name": "Women's Handbag & Purse",
        "keywords": ["bag", "handbag", "tote", "sling", "clutch", "crossbody", "wallet", "backpack", "purse", "potli", "satchel"],
        "occasion": "daily office, shopping days, brunch meetups, and travel",
        "craftsmanship": "Crafted with durable water-resistant vegan leather, reinforced seams, and premium metal hardware",
        "styling": "Effortlessly pairs with both formal workwear and casual weekend outfits.",
        "hashtags": "#Handbags #WomensTote #SlingBag #DesignerBag #BagLover #AccessoriesForWomen"
    },
    {
        "id": "earrings",
        "name": "Women's Earrings & Jhumkas",
        "keywords": ["earring", "jhumka", "jhumki", "stud", "hoop", "dangler", "chandbali", "ear drop"],
        "occasion": "weddings, festive celebrations, dinner dates, and everyday elegance",
        "craftsmanship": "Artfully crafted with hypoallergenic posts, detailed stone embellishments, and radiant plating",
        "styling": "Wear with festive sarees, lehengas, or keep it subtle with daily ethnic kurtis.",
        "hashtags": "#Earrings #Jhumkas #StatementEarrings #IndianJewellery #JewelleryLovers #Chandbalis"
    },
    {
        "id": "necklaces",
        "name": "Necklace & Jewellery Set",
        "keywords": ["necklace", "choker", "pendant", "chain", "jewellery set", "jewelry set", "jewellery", "jewelry", "mangalsutra", "kundan"],
        "occasion": "weddings, engagements, anniversary celebrations, and festive parties",
        "craftsmanship": "Features finely set kundan, crystals, or pearls with secure clasp mechanisms and rich polish",
        "styling": "Pairs exquisitely with deep-neck blouses, silk sarees, and regal bridal lehengas.",
        "hashtags": "#NecklaceDesign #ChokerNecklace #JewellerySet #EthnicJewellery #BridalJewellery"
    },
    {
        "id": "bracelets",
        "name": "Bracelets & Bangles",
        "keywords": ["bracelet", "bangle", "kada", "cuff", "charm bracelet", "wristband"],
        "occasion": "parties, traditional poojas, festive family events, and gifting",
        "craftsmanship": "Crafted with smooth rounded edges, skin-friendly plating, and durable locking clasps",
        "styling": "Stack with matching rings or wear solo as a minimalist wrist statement piece.",
        "hashtags": "#Bracelet #Bangles #Kada #DesignerJewellery #FashionAccessories #WristJewellery"
    },
    {
        "id": "rings_accessories",
        "name": "Women's Rings & Accessories",
        "keywords": ["nose pin", "ring", "toe ring", "belt", "kamarbandh", "kamarband", "dupatta", "scarf", "shawl", "stole", "brooch", "hair band", "hair accessory"],
        "occasion": "festivals, wedding celebrations, party nights, and daily accent styling",
        "craftsmanship": "Expertly crafted with fine detailing, durable construction, and smooth comfortable wear",
        "styling": "The perfect accent piece to complete both ethnic and contemporary modern looks.",
        "hashtags": "#FashionAccessories #EthnicAccessories #StatementRings #DupattaStyle #StyleDetails"
    },
    {
        "id": "face_makeup",
        "name": "Face Makeup & Cosmetics",
        "keywords": ["foundation", "concealer", "compact", "powder", "primer", "blush", "highlighter", "contour", "bb cream", "cc cream", "cream", "bronzer"],
        "occasion": "daily beauty routines, festive touch-ups, glam party looks, and camera-ready radiance",
        "craftsmanship": "Formulated with lightweight, blendable, non-comedogenic ingredients for a natural, seamless finish",
        "styling": "Apply on clean, moisturized skin and blend gently for all-day luminous, streak-free wear.",
        "hashtags": "#FaceMakeup #Foundation #FlawlessSkin #BeautyRoutine #MakeupEssentials #GlowMakeup"
    },
    {
        "id": "lip_makeup",
        "name": "Lipstick & Lip Care",
        "keywords": ["lipstick", "lip gloss", "lip liner", "lip balm", "lip tint", "liquid lipstick", "lip crayon"],
        "occasion": "everyday wear, festive celebrations, office meetings, and party glamour",
        "craftsmanship": "Formulated with rich pigments and nourishing moisturizing agents for smudge-proof, hydrated lips",
        "styling": "Glide directly on lips or outline with a matching lip liner for precise, defined shape.",
        "hashtags": "#Lipstick #LipGloss #LipstickLove #MatteLipstick #LipCare #BeautyTips"
    },
    {
        "id": "eye_makeup",
        "name": "Eye Makeup",
        "keywords": ["eyeliner", "kajal", "mascara", "eyeshadow", "eye shadow", "brow", "eyebrow", "lash"],
        "occasion": "bold festive looks, smokey evening eyes, and subtle day definition",
        "craftsmanship": "Formulated with waterproof, smudge-resistant pigments for smooth glide and high precision",
        "styling": "Pair with your favorite lip shade and sculpted brows to make your eyes pop.",
        "hashtags": "#EyeMakeup #Eyeliner #Kajal #Mascara #BoldEyes #BeautyInspiration"
    },
    {
        "id": "skincare",
        "name": "Women's Skincare",
        "keywords": ["serum", "sunscreen", "moisturizer", "cleanser", "face wash", "toner", "face cream", "lotion", "body lotion", "sheet mask", "scrub"],
        "occasion": "morning and evening daily skincare routines, skin barrier repair, and sun protection",
        "craftsmanship": "Dermatologically tested formula packed with active ingredients to nourish and protect skin health",
        "styling": "Use consistently as part of your AM/PM routine for a healthy, glowing complexion.",
        "hashtags": "#SkincareRoutine #HealthySkin #GlowSkin #SkincareEssentials #DermatologyTested #SelfCare"
    },
    {
        "id": "fragrance",
        "name": "Women's Perfume & Fragrance",
        "keywords": ["perfume", "fragrance", "mist", "deodorant", "cologne", "body spray", "attar"],
        "occasion": "special evenings, dates, daily freshness, and festive occasions",
        "craftsmanship": "Artfully blended with captivating top, heart, and base notes for a long-lasting signature trail",
        "styling": "Spritz onto pulse points such as wrists, neck, and behind ears for lingering all-day projection.",
        "hashtags": "#WomensPerfume #FragranceCollection #BodyMist #SignatureScent #LongLastingPerfume"
    },
    {
        "id": "lingerie",
        "name": "Women's Lingerie & Sleepwear",
        "keywords": ["bra", "bralette", "panty", "lingerie", "night suit", "nightwear", "nighty", "sleepwear", "robe", "shapewear", "camisole", "babydoll", "nightdress"],
        "occasion": "cozy night sleep, lazy weekend lounging, and smooth everyday innerwear support",
        "craftsmanship": "Tailored with seamless soft stretch fabric, gentle elastic bands, and breathable comfort",
        "styling": "Provides invisible comfort under everyday clothes or ultimate relaxation at home.",
        "hashtags": "#WomensLingerie #Sleepwear #ComfortBra #NightSuit #LoungewearStyle #CozyNights"
    }
]

PROMO_PATTERN = re.compile(
    r'(?i)\b(loot|deals?|discounts?|\d+%\s*off|%\s*off|price\s*drop|offers?|sales?|under\s*₹?\d+|flat\s*\d+%|save\s*₹?\d+|today\s*only|best\s*deal|hot\s*deal|exclusive|limited\s*time|amazon\s*sale|deal\s*price|great\s*you\s*cant\s*miss)\b'
)

TRAILING_STOPWORDS = re.compile(r'(?i)\b(with|for|and|in|at|of|to|the|a|an|by|from|or|on)\s*$', re.IGNORECASE)

def is_banned(title, link):
    t_lower = (title + " " + link).lower()
    
    # Exclude non-fashion junk
    NON_FASHION = [
        "gripper", "gym", "dumbbell", "exercise", "equipment", "fitness", "wrist",
        "laptop", "oled", "ssd", "ram", "intel", "processor", "tablet", "mouse",
        "keyboard", "cable", "charger", "earbuds", "headphone", "speaker", "tv",
        "idol", "murti", "brass", "shiva", "ganesha", "pooja", "god", "mandir",
        "drill", "drain", "downlight", "microwave", "shaving", "trimmer", "glove"
    ]
    if any(nf in t_lower for nf in NON_FASHION):
        return True
        
    # Corrupt titles from old scrapers
    CORRUPT_PATTERNS = [
        "amazon —", "today only", "suppar sleave", "trendmalls", "digital shopee",
        "rock paper scissors", "great you cant miss"
    ]
    if any(cp in t_lower for cp in CORRUPT_PATTERNS):
        return True
        
    # Check for strictly male-only clothing (do not match if 'women' is present)
    has_female = bool(re.search(r'\b(women|woman|women\'s|womens|girl|girls|lady|ladies|she|her)\b', t_lower))
    has_male_only = bool(re.search(r'\b(men|men\'s|mens|male|boys)\b', t_lower)) and not has_female
    if has_male_only:
        return True
        
    return False

def clean_title(raw_title):
    if not raw_title: return ""
    # Strip residue from old description leak
    t = raw_title.split(". A beautifully tailored")[0].split(". Crafted for women")[0]
    # Remove bracketed promos: (60% OFF), [Pack of 2], etc.
    t = re.sub(r'[\(\[\{][^\)\]\}]*(?:%|off|deal|loot|save|free|festival|sale)[^\)\]\}]*[\)\]\}]', '', t, flags=re.IGNORECASE)
    # Remove promo keywords
    t = PROMO_PATTERN.sub('', t)
    # Remove emojis
    t = re.sub(r'[⚡🔥💥✨🛍️🎉🏷️👰🌸❤️👗💍👠💄]', '', t)
    # Remove price text (at ₹149, for Rs 599)
    t = re.sub(r'(?i)\b(at|for|rs\.?|inr)\s*₹?\s*\d+(?:,\d+)*\b', '', t)
    # Clean up multi-pipes / keyword stuffing (e.g. |top for Women|Backless Tops...)
    if "|" in t:
        parts = [p.strip() for p in t.split("|") if p.strip()]
        t = parts[0]
    # Remove trailing/leading junk characters
    t = re.sub(r'[\s\-:,|/–—.]+$', '', t).strip(' -:,|/–—.')
    t = re.sub(r'\s+', ' ', t).strip()
    
    # Strip trailing stopwords (e.g. "Dress for", "Top with")
    for _ in range(3):
        t = TRAILING_STOPWORDS.sub('', t).strip(' -:,|/–—.')
        
    # Cap title cleanly at word boundary under 95 chars (Pinterest optimal length 60-95)
    if len(t) > 95:
        t = t[:95].rsplit(' ', 1)[0].strip(' -:,|/–—.')
        
    return t

def classify(title):
    for cat in TAXONOMY:
        for kw in cat["keywords"]:
            pattern = r'\b' + re.escape(kw) + r'(?:s|es)?\b'
            if re.search(pattern, title, re.IGNORECASE):
                return cat
    return None

def process_feed(feed_path):
    if not os.path.exists(feed_path):
        print(f"Skipping {feed_path} (not found)")
        return
        
    tree = ET.parse(feed_path)
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        return
        
    items = channel.findall("item")
    print(f"\nProcessing {os.path.basename(feed_path)} (Initial items: {len(items)})...")
    
    seen_links = set()
    valid_items = []
    dropped_count = 0
    
    for it in items:
        link_elem = it.find("link")
        link = (link_elem.text if link_elem is not None else "").strip()
        if not link or link in seen_links:
            dropped_count += 1
            continue
            
        raw_title = (it.findtext("title") or "").strip()
        
        # Check against banned / junk / corrupt phrases
        if is_banned(raw_title, link):
            dropped_count += 1
            continue
            
        cleaned_t = clean_title(raw_title)
        
        # Must have at least 3 descriptive words in title
        if len(cleaned_t.split()) < 3:
            dropped_count += 1
            continue
            
        # Accurately classify
        cat = classify(cleaned_t)
        if not cat:
            # Fall back to general women's fashion only if it clearly mentions women / fashion / style
            if any(w in cleaned_t.lower() for w in ["women", "womens", "lady", "ladies", "girls", "fashion"]):
                cat = {
                    "id": "fashion_apparel",
                    "name": "Women's Fashion Apparel",
                    "occasion": "versatile celebrations, family gatherings, and everyday elegance",
                    "craftsmanship": "Crafted with soft comfortable fabric, clean stitching, and versatile styling",
                    "styling": "Pair with your favorite accessories, footwear, and minimal styling for a graceful look.",
                    "hashtags": "#WomensFashion #OOTD #FashionInspo #DailyStyle #IndianFashion"
                }
            else:
                dropped_count += 1
                continue
                
        seen_links.add(link)
        
        # Generate Native SEO Description
        # Extract store hint
        store_name = "Myntra" if "myn-" in link or "myntra" in link.lower() else ("Flipkart" if "fk-" in link or "flipkart" in link.lower() else "Amazon")
        
        lead_str = f"{cleaned_t}."
        seo_description = (
            f"{lead_str} "
            f"An authentic {cat['name']} crafted for women seeking effortless elegance, refined tailoring, and modern style. "
            f"Ideal for {cat['occasion']}. {cat['craftsmanship']}. {cat['styling']} "
            f"Available on {store_name} with verified doorstep delivery and authentic quality assurance. "
            f"{cat['hashtags']}"
        )
        
        # Update XML elements
        title_elem = it.find("title")
        if title_elem is not None:
            title_elem.text = cleaned_t
        else:
            ET.SubElement(it, "title").text = cleaned_t
            
        desc_elem = it.find("description")
        if desc_elem is not None:
            desc_elem.text = seo_description
        else:
            ET.SubElement(it, "description").text = seo_description
            
        valid_items.append(it)
        
    # Replace items in channel
    for it in channel.findall("item"):
        channel.remove(it)
        
    for it in valid_items:
        channel.append(it)
        
    tree.write(feed_path, encoding="utf-8", xml_declaration=True)
    print(f"✨ Finished {os.path.basename(feed_path)}: {len(valid_items)} high-quality items saved (Dropped {dropped_count} junk/duplicates).")

if __name__ == "__main__":
    process_feed(PINTEREST_FEED)
    process_feed(WOMEN_FEED)
