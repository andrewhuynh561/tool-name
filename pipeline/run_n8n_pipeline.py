import os
import sys
import csv
import re
import math
from pathlib import Path


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    # ── Parse CLI flags ──────────────────────────────────────────────────────
    # ── Parse CLI flags ──────────────────────────────────────────────────────
    args = sys.argv[1:]
    delta_mode = '--delta' in args
    store_arg = None
    input_paths = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--store' and i + 1 < len(args):
            store_arg = args[i + 1].lower()
            i += 2
        elif a.startswith('--'):
            i += 1
        else:
            input_paths.append(a)
            i += 1

    # Store Configuration
    is_store2 = store_arg in ('store2', 'augoodvantage', 'agv', 'store_2')
    store_name = 'AuGoodVantage' if is_store2 else 'PivotLiving'
    store_url = 'https://www.ebay.com.au/str/augoodvantage' if is_store2 else 'https://www.ebay.com.au/str/pivotliving'
    sku_prefix = 'AGV-' if is_store2 else 'DSZ-'
    watermark_public_id = 'OpenAI_Playground_2026-09-05_at_21.54.57' if is_store2 else 'ChatGPT_Image_Aug_26_2026_12_31_37_AM'

    print(f"🏪 Active Store: {store_name} ({sku_prefix}) | Watermark: {watermark_public_id}")

    if not input_paths:
        downloads_dir = Path("C:/Users/andre/Downloads")
        general_files = sorted(downloads_dir.rglob("General_*.csv"), key=os.path.getmtime, reverse=True)
        if general_files:
            input_paths = [str(general_files[0])]

    parsed_items = []
    feed_keys = []
    for ip in input_paths:
        if os.path.exists(ip):
            print(f"📖 Reading Input Feed File: {ip}")
            feed_keys.append(Path(ip).stem.split('T')[0])
            with open(ip, mode="r", encoding="utf-8-sig", errors="ignore") as f:
                reader = csv.DictReader(f)
                parsed_items.extend(list(reader))
        else:
            print(f"⚠️ File not found: {ip}")

    # Remove intra-batch duplicates by SKU
    seen_in_batch = set()
    deduped_items = []
    for item in parsed_items:
        s = item.get('SKU', item.get('ProductID', '')).strip()
        if s and s not in seen_in_batch:
            seen_in_batch.add(s)
            deduped_items.append(item)
    parsed_items = deduped_items

    print(f"Parsed {len(parsed_items)} unique items from input feed(s).")
    if delta_mode:
        print("🔄 DELTA MODE: will only process NEW SKUs since last snapshot.")

    # ── DELTA: subtract SKUs already processed in a previous run ─────────────
    SNAPSHOT_PATH = Path("C:/Users/andre/Ebay/pipeline/snapshots")
    SNAPSHOT_PATH.mkdir(parents=True, exist_ok=True)
    feed_key = feed_keys[0] if feed_keys else "General_20260905"

    if is_store2:
        snapshot_file = SNAPSHOT_PATH / "store2_seen_skus.txt"
    else:
        snapshot_file = SNAPSHOT_PATH / f"{feed_key}_seen_skus.txt"

    if delta_mode:
        seen_skus = set()
        if snapshot_file.exists():
            seen_skus = set(snapshot_file.read_text(encoding='utf-8').splitlines())
        sku_col = next((k for k in (parsed_items[0].keys() if parsed_items else [])
                        if 'sku' in k.lower() or k in ('ProductID', 'SupplierSKU')), 'SKU')
        before = len(parsed_items)
        parsed_items = [r for r in parsed_items
                        if r.get(sku_col, '').strip() not in seen_skus]
        print(f"📊 Delta: {before} total → {len(parsed_items)} NEW "
              f"({before - len(parsed_items)} already seen).")

    # ── Load existing active eBay listings for deduplication ─────────────────
    active_skus = set()
    possible_active_paths = []
    if is_store2:
        possible_active_paths = [
            str(SNAPSHOT_PATH / "store2_seen_skus.txt")
        ]
    else:
        possible_active_paths = [
            "c:/Users/andre/Ebay/pipeline/snapshots/seen_skus.txt",
            "c:/Users/andre/Ebay/pipeline/snapshots/active_skus_20260903.txt",
            "c:/Users/andre/Ebay/pipeline/active_listings.csv",
            "c:/Users/andre/Ebay/active_listings.csv",
        ]
        downloads_dir = Path("C:/Users/andre/Downloads")
        for report in downloads_dir.rglob("*active-listings-report*.csv"):
            possible_active_paths.insert(0, str(report))
        for report in downloads_dir.rglob("*upload*.csv"):
            if not report.name.startswith("output_ebay_upload"):
                possible_active_paths.insert(0, str(report))

    for path_str in possible_active_paths:
        if os.path.exists(path_str):
            if Path(path_str).name.startswith("output_ebay_upload"):
                continue
            print(f"🔍 Scanning Active eBay Listings: {path_str}")
            if path_str.endswith(".txt"):
                with open(path_str, mode="r", encoding="utf-8", errors="ignore") as tf:
                    for line in tf:
                        cleaned = line.strip().upper()
                        if cleaned:
                            active_skus.add(cleaned)
                            if cleaned.startswith(sku_prefix):
                                active_skus.add(cleaned.replace(sku_prefix, ""))
            else:
                with open(path_str, mode="r", encoding="utf-8-sig", errors="ignore") as af:
                    areader = csv.reader(af)
                    for row in areader:
                        for cell in row:
                            cleaned = cell.replace('"', '').strip().upper()
                            if cleaned.startswith(sku_prefix) or len(cleaned) > 3:
                                active_skus.add(cleaned)
                                if cleaned.startswith(sku_prefix):
                                    active_skus.add(cleaned.replace(sku_prefix, ""))
    print(f"📦 Total Loaded {len(active_skus)} existing active SKUs for deduplication.\n")

    # ── Master Config ─────────────────────────────────────────────────────────
    CONFIG = {
        'cloudinaryCloudName': 'smqochzy',
        'watermarkPublicId': watermark_public_id,
        'watermarkGravity': 'south',
        'watermarkWidthPct': 100,
        'watermarkXOffset': 0,
        'watermarkYOffset': 0,
        'watermarkOpacity': 95,
        'pricingMode': 'rrp_plus_5',
        'markupMultiplier': 1.35,
        'flatFee': 5.00,
        'ebayFeeRate': 0.135,
        'applyEbayFeeBuffer': True,
        'includeFreeShipping': True,
        'applyActiveRebate': True,
        'minimumListingPrice': 9.99,
        'charmPrice': False if is_store2 else True,
        'maxListingQuantity': 1,
        'storeName': store_name,
        'storeUrl': store_url,
        'skuPrefix': sku_prefix,
        'isStore2': is_store2,
    }

    # ── Category Mapping (Verified 2026 eBay AU Leaf Category IDs — NO DUPLICATES) ──
    # Priority: first matching keyword wins. More specific terms before general ones.
    CATEGORY_MAP = {
        # ─── Smart Watch / Wearables ─────────────────────────────────────────
        'smartwatch':            '182068',
        'smart watch':           '182068',
        'fitbit':                '182068',
        'watch band':            '182068',
        'watch strap':           '182068',
        'wristband':             '182068',
        # ─── Fishing & Marine ─────────────────────────────────────────────────
        'tackle box':            '179998',
        'tackle storage':        '179998',
        'tackleboxes':           '179998',
        'tackle':                '179998',
        'lure':                  '179995',
        'bait':                  '179995',
        'fishing':               '14104',
        'fish scaler':           '20632',
        'fish scale':            '20632',
        'aquarium':              '20755',
        'fish tank':             '20755',
        'boating':               '26443',
        'boat':                  '26443',
        'marine':                '26443',
        'yacht':                 '26443',
        'canoe':                 '26443',
        'paddle':                '26443',
        'diving':                '1300',
        'snorkel':               '1300',

        # ─── Sports & Trampoline ──────────────────────────────────────────────
        'trampoline':            '140974',
        'tennis':                '159139',
        'racquet':               '159139',
        'water bladder':         '181382',
        'golf':                  '18933',
        'tent':                  '36118',
        'canopy':                '36118',
        'sun shelter':           '36118',
        'sleeping pad':          '181378',
        'sleeping mat':          '181378',
        'air mattress':          '181378',
        'cooler pad':            '177074',
        'coin collection':       '11116',
        'coin holder':           '11116',
        'rebounder net':         '158928',
        'patch':                 '3118',
        'repair tape':           '3118',

        # ─── Pet Supplies ────────────────────────────────────────────────────
        'silvervine':            '177789',
        'cat litter':            '177789',
        'litter scoop':          '177789',
        'cat bowl':              '177789',
        'cat fountain':          '177789',
        'cat toy':               '177789',
        'cat harness':           '177789',
        'bird nest':             '177789',
        'dog harness':           '177794',
        'dog nail':              '177794',
        'dog ear':               '177794',
        'dog collar':            '177794',
        'dog lead':              '177794',
        'dog carrier':           '177794',
        'dog crate':             '177794',
        'dog training':          '177794',
        'pet waste':             '177794',
        'pet harness':           '177794',
        'pet fountain':          '177794',
        'pet water':             '177794',
        'suction cup dog':       '177794',
        'chew ball':             '177794',
        'tug rope':              '177794',
        'dog toy':               '177794',
        'grooming':              '177794',

        # ─── Cameras & Optics ────────────────────────────────────────────────
        'digital camera':        '31388',
        'vlog camera':           '31388',
        'action camera':         '31388',
        'binoculars':            '31724',
        'monocular':             '31724',
        'night vision':          '31724',
        'telescope':             '31724',

        # ─── Audio ───────────────────────────────────────────────────────────
        'headphones':            '112529',
        'headset':               '112529',
        'over ear':              '112529',
        'in ear':                '112529',
        'earbuds':               '112529',
        'earphone':              '112529',
        'speaker':               '96954',
        'radio':                 '96954',

        # ─── Computer / Keyboard / Electronics ───────────────────────────────
        'keyboard':              '33883',
        'tablet keyboard':       '33883',
        'bluetooth keyboard':    '33883',
        'laptop stand':          '33883',
        'mouse':                 '33883',

        # ─── Calculators / Styluses / Office ─────────────────────────────────
        'calculator':            '11714',
        'scientific function':   '11714',
        's pen':                 '11714',
        'stylus pen':            '11714',
        'office supply':         '11714',

        # ─── Phone / Mobile Accessories ──────────────────────────────────────
        'charging cable':        '35190',
        'retractable cable':     '35190',
        'usb cable':             '35190',
        'phone charger':         '35190',
        'phone stand':           '166094',
        'phone holder':          '166094',
        'car mount':             '166094',
        'dash mount':            '166094',
        'wireless charger':      '166094',

        # ─── Health, Fitness & Sports ─────────────────────────────────────────
        'massage':               '36449',
        'massager':              '36449',
        'brace':                 '36449',
        'supports':              '36449',
        'knee brace':            '36449',
        'back support':          '36449',
        'posture':               '36449',
        'kegel':                 '15280',
        'pelvic':                '15280',
        'yoga':                  '158928',
        'pilates':               '158928',
        'fitness':               '158928',
        'gym':                   '158928',
        'exercise':              '158928',
        'push up':               '158928',
        'resistance band':       '158928',
        'jump rope':             '158928',

        # ─── Hair & Personal Care ─────────────────────────────────────────────
        'hair dryer':            '31413',
        'hair straightener':     '31413',
        'hair curler':           '31413',
        'trimmer':               '31770',
        'shaver':                '31770',
        'flosser':               '31770',
        'toothbrush':            '31770',
        'shaving':               '31770',

        # ─── Kitchen & Cooking ────────────────────────────────────────────────
        'coffee machine':        '20632',
        'coffee maker':          '20632',
        'espresso':              '20632',
        'waffle maker':          '20632',
        'toaster':               '20632',
        'kitchen utensil':       '20632',
        'kitchen tool':          '20632',
        'chopper':               '20632',
        'grater':                '20632',
        'whisk':                 '20632',
        'measuring':             '20632',
        'soap dispenser':        '20632',
        'cookware':              '20632',
        'food storage':          '177069',
        'storage container':     '177069',
        'lunch box':             '177069',
        'bbq brush':             '177066',
        'bbq tool':              '177066',
        'grill brush':           '177066',
        'bbq':                   '177066',
        'grill':                 '177066',

        # ─── Home & Garden ────────────────────────────────────────────────────
        'pillow':                '20563',
        'cushion':               '20563',
        'blanket':               '20572',
        'throw':                 '20572',
        'electric blanket':      '20572',
        'heated mattress':       '20572',
        'mattress pad':          '20572',
        'towel':                 '20572',
        'placemat':              '20572',
        'placemat bamboo':       '20572',
        'bamboo placemat':       '20572',
        'table linen':           '20572',
        'diffuser':              '20561',
        'aroma':                 '20561',
        'humidifier':            '20561',
        'fragrance':             '20561',
        'candle':                '20561',
        'lamp':                  '20702',
        'wall hook':             '20635',
        'hook':                  '20635',
        'outdoor light':         '20702',
        'solar light':           '20702',
        'night light':           '20702',
        'fairy light':           '20702',
        'projection light':      '20702',
        'cleaning':              '20636',
        'scrubber':              '20636',
        'drain':                 '20636',

        # ─── Appliances ───────────────────────────────────────────────────────
        'electric heater':       '43509',
        'heater':                '43509',
        'vacuum cleaner':        '42255',
        'stick vacuum':          '42255',
        'cordless vacuum':       '42255',
        'air conditioner':       '43509',
        'fan':                   '43509',

        # ─── Tools ────────────────────────────────────────────────────────────
        'deburring':             '42255',
        'hand tool':             '42255',
        'engraver':              '42255',
        'drill':                 '42255',
        'work safety':           '42255',
        'tool':                  '42255',

        # ─── Outdoor, Camping, Travel ──────────────────────────────────────────
        'camping':               '181378',
        'hammock':               '181378',
        'caravan':               '74860',
        'rv cowl':               '74860',
        'rv cover':              '74860',
        'rv accessory':          '74860',
        'hiking':                '181380',
        'trekking':              '181380',
        'water bag':             '181382',
        'hydration':             '181382',
        'chest rig':             '180126',
        'tactical':              '180126',
        'earplugs':              '181379',
        'headlamp':              '16037',
        'flashlight':            '16037',
        'torch':                 '16037',
        'backpack':              '169291',
        'bicycle bag':           '169291',

        # ─── Clothing & Accessories ───────────────────────────────────────────
        'wallet':                '2996',
        'purse':                 '169291',
        'bag':                   '169291',
        'scarf':                 '45230',
        'shawl':                 '45230',
        'cap':                   '45230',
        'goggle':                '45230',
        'sewing':                '3118',
        'jewellery':             '10968',

        # ─── Car Accessories ──────────────────────────────────────────────────
        'car vacuum':            '169420',
        'car charger':           '169420',
        'seat cushion':          '169420',
        'car accessory':         '169420',
        'auto':                  '169420',
        'rv':                    '169420',

        # ─── Baby & Kids ──────────────────────────────────────────────────────
        'building toy':          '19016',
        'building block':        '19016',
        'kids toy':              '19016',
        'children':              '19016',

        # ─── Bikes ────────────────────────────────────────────────────────────
        'bike':                  '58100',
        'bicycle':               '58100',
        'horn':                  '58100',

        # ─── Skin Care & Beauty ───────────────────────────────────────────────
        'skincare':              '31413',
        'face mask':             '31413',
        'facial cleanser':       '31413',
        'skin care':             '31413',

        # ─── TV / Entertainment ───────────────────────────────────────────────
        'television':            '20565',
        'tv stand':              '20565',

        # ─── Gardening ────────────────────────────────────────────────────────
        'gardening':             '29524',
        'moss':                  '181036',
        'turf':                  '181036',

        # ─── Shower / Bathroom ────────────────────────────────────────────────
        'shower':                '181379',

        # ─── Lunch & Cooler ───────────────────────────────────────────────────
        'lunch bag':             '177074',
        'cooler':                '177074',

        # ─── Seasonal ─────────────────────────────────────────────────────────
        'christmas':             '170091',
        'halloween':             '170091',
        'costume':               '170091',

        # ─── Keys & Accessories ───────────────────────────────────────────────
        'keychain':              '45230',

        # ─── Default fallback ─────────────────────────────────────────────────
        'default':               '20632'
    }

    # ── Item Specs Extractor ──────────────────────────────────────────────────
    def extract_specs(item, clean_title):
        desc = item.get('Description', '')
        title = item.get('Title', '')
        text = f"{title} {desc}".lower()

        material = 'High Quality Material'
        mat_matches = [
            ('carbon fiber', 'Carbon Fiber'), ('fiberglass', 'Fiberglass'),
            ('stainless steel', 'Stainless Steel'), ('aluminum alloy', 'Aluminum Alloy'),
            ('aluminium', 'Aluminium Alloy'), ('pu leather', 'PU Leather'),
            ('memory foam', 'Memory Foam'), ('oxford cloth', 'Oxford Fabric'),
            ('oxford fabric', 'Oxford Fabric'), ('canvas', 'Canvas'),
            ('corduroy', 'Corduroy'), ('abs plastic', 'ABS Plastic'),
            ('abs', 'ABS Plastic'), ('silicone', 'Silicone'),
            ('tpe', 'TPE'), ('pvc', 'Heavy Duty PVC'),
        ]
        for k, v in mat_matches:
            if k in text:
                material = v
                break

        colour = 'Multicoloured'
        colours = ['Black', 'White', 'Grey', 'Gray', 'Blue', 'Pink', 'Purple',
                   'Green', 'Silver', 'Gold', 'Yellow', 'Khaki', 'Beige', 'Red', 'Orange']
        for c in colours:
            if re.search(r'\b' + c + r'\b', clean_title, re.I):
                colour = 'Grey' if c == 'Gray' else c
                break

        power = 'Manual / Non-Electric'
        if 'solar' in text:
            power = 'Solar Powered'
        elif 'usb rechargeable' in text or 'rechargeable' in text:
            power = 'USB Rechargeable Battery'
        elif 'usb powered' in text or 'usb' in text:
            power = 'USB Powered'
        elif 'battery' in text:
            power = 'Battery Powered'

        dept = 'Unisex Adults'
        if re.search(r'\b(women|woman|ladies|girls)\b', text, re.I):
            dept = 'Women'
        elif re.search(r'\b(men|man|gentlemen|boys)\b', text, re.I):
            dept = 'Men'

        style = 'Modern'
        if 'tote' in text:
            style = 'Tote'
        elif 'shoulder' in text:
            style = 'Shoulder Bag'
        elif 'backpack' in text:
            style = 'Backpack'
        elif 'tactical' in text:
            style = 'Tactical'

        feats = []
        for kw in ['Portable', 'Lightweight', 'Rechargeable', 'Waterproof', 'Adjustable',
                   'Foldable', 'Wireless', 'Multi-function']:
            if kw.lower() in text:
                feats.append(kw)
        features_str = ', '.join(feats[:5]) if feats else 'Durable, Easy to Use'

        sku = item.get('SKU', item.get('ProductID', ''))
        subcat = item.get('Subcategory', item.get('Category', 'Accessories'))

        return {
            'C:Brand':           'Unbranded',
            'C:Model':           f'{sku_prefix}{sku}',
            'C:Type':            subcat,
            'C:Material':        material,
            'C:Colour':          colour,
            'C:Department':      dept,
            'C:Style':           style,
            'C:Power Source':    power,
            'C:Features':        features_str,
            'C:MPN':             f'{sku_prefix}{sku}',
            'C:Size':            'One Size',
            'C:Compatible Brand':'Universal',
            'C:Stove Type Compatibility': 'Not Applicable',
        }

    # ── Cloudinary Watermark Helper ───────────────────────────────────────────
    def build_cloudinary_url(image_url):
        cloud = CONFIG['cloudinaryCloudName']
        wm_id = CONFIG['watermarkPublicId']
        gravity = CONFIG['watermarkGravity']
        width = CONFIG['watermarkWidthPct']
        x = CONFIG['watermarkXOffset']
        y = CONFIG['watermarkYOffset']
        opacity = CONFIG['watermarkOpacity']
        transform = (f"l_{wm_id},w_{width / 100:.2f},c_scale,"
                     f"g_{gravity},x_{x},y_{y},o_{opacity},fl_relative")
        return f"https://res.cloudinary.com/{cloud}/image/fetch/{transform}/{image_url}"

    # ── Title Formatting Helper (Word-boundary safe, 80 chars max) ───────────
    def format_title(raw_t, is_s2):
        tc = re.sub(r'^[A-Z0-9]{2,}-[A-Z0-9-]+\s+', '', raw_t, flags=re.I).strip()
        tc = re.sub(r'\s+', ' ', tc)
        if is_s2:
            tc = re.sub(r'^(?:Landhoow|Weisshorn|Everfit|Alritz|JIALWEN|TAMOSH)\s*[:\-]?\s*', '', tc, flags=re.I).strip()
            tc = re.sub(r'\b(?:AU Stock|AU Fast Post)\b', '', tc, flags=re.I).strip()
            tc = re.sub(r'\s+', ' ', tc)
            sfx = ' AU Fast Post'
        else:
            tc = re.sub(r'\b(?:AU Stock|AU Fast Post)\b', '', tc, flags=re.I).strip()
            tc = re.sub(r'\s+', ' ', tc)
            sfx = ' AU Stock'

        if len(tc) + len(sfx) <= 80:
            return tc + sfx
        else:
            max_len = 80 - len(sfx)
            truncated = tc[:max_len]
            last_space = truncated.rfind(' ')
            return (truncated[:last_space] if last_space > 30 else truncated) + sfx

    # ── Prohibited Items Filter ───────────────────────────────────────────────
    PROHIBITED_KEYWORDS = [
        'medical device', 'fda', 'therapeutic', 'clinical', 'prescription',
        'eeg', 'ecg', 'pulse oximeter', 'blood pressure monitor', 'glucose meter',
        'nebulizer', 'defibrillator', 'surgical', 'stethoscope',
    ]

    # ── Main Processing Loop ──────────────────────────────────────────────────
    ebay_rows = []
    skipped_count = 0
    prohibited_count = 0

    # Detect column names dynamically
    sample = parsed_items[0] if parsed_items else {}
    sku_col = next((k for k in sample if k in ('SKU', 'ProductID', 'SupplierSKU')), 'SKU')
    title_col = next((k for k in sample if k in ('Title', 'ProductName', 'Name')), 'Title')
    cost_col = next((k for k in sample if k in ('Cost per item', 'Price', 'Cost', 'RRP', 'WholesalePrice')), 'Cost per item')
    desc_col = next((k for k in sample if k in ('Description', 'ProductDescription')), 'Description')
    rrp_col = next((k for k in sample if k.upper() == 'RRP' or 'rrp' in k.lower()), 'RRP')
    cat_col = next((k for k in sample if k == 'Category'), 'Category')
    subcat_col = next((k for k in sample if k == 'Subcategory'), 'Subcategory')
    subsubcat_col = next((k for k in sample if k == 'Sub_subcategory'), 'Sub_subcategory')
    qty_col = next((k for k in sample if k in ('QOH', 'StockQty', 'Quantity', 'Stock')), 'QOH')

    # Detect image columns
    img_cols = [k for k in sample if re.search(r'image|photo|img|pic', k, re.I)]
    if not img_cols:
        img_cols = [k for k in sample if re.match(r'Image\d+|Pic\d+', k)]

    cloudinary_cloud = CONFIG['cloudinaryCloudName']
    watermark_id = CONFIG['watermarkPublicId']
    watermark_layer = (f"l_{watermark_id},w_1.00,c_scale,"
                       f"g_{CONFIG['watermarkGravity']},x_0,y_0,"
                       f"o_{CONFIG['watermarkOpacity']},fl_relative")

    for index, item in enumerate(parsed_items):
        sku = item.get(sku_col, '').strip()
        if not sku:
            continue

        sku_upper = sku.upper()
        dsz_sku = f"{sku_prefix}{sku_upper}"

        # Deduplication
        if sku_upper in active_skus or dsz_sku in active_skus:
            skipped_count += 1
            continue

        raw_title = item.get(title_col, '').strip()
        cat = item.get(cat_col, '').strip()
        subcat = item.get(subcat_col, '').strip()
        subsubcat = item.get(subsubcat_col, '').strip()
        raw_desc = item.get(desc_col, '').strip()
        cost_raw = item.get(cost_col, '0').strip()

        # Prohibited filter: only match actual medical instruments using word boundaries,
        # ignoring shipping restriction tables and standard disclaimers
        full_text_lower = f"{raw_title} {raw_desc} {cat} {subcat}".lower()
        clean_text_check = re.sub(r'<details>.*?</details>', '', full_text_lower, flags=re.S)
        clean_text_check = re.sub(r'not (?:intended for|designed for|a) (?:medical|therapeutic)[^.]*', '', clean_text_check)
        clean_text_check = re.sub(r'leisure accessory only[^.]*', '', clean_text_check)
        if any(re.search(r'\b' + re.escape(pk) + r'\b', clean_text_check) for pk in PROHIBITED_KEYWORDS):
            prohibited_count += 1
            continue

        # Title cleanup & 80-char Cassini format
        final_title = format_title(raw_title, is_store2)

        # Pricing: RRP + $5.00 formula
        cost = float(re.sub(r'[^0-9.]', '', cost_raw) or '0')
        rrp_raw = item.get(rrp_col, '').strip()
        rrp = float(re.sub(r'[^0-9.]', '', rrp_raw) or '0')
        if rrp <= 0:
            rrp = cost * 1.5 if cost > 0 else CONFIG['minimumListingPrice']

        flat_fee = CONFIG['flatFee']
        ebay_fee = CONFIG['ebayFeeRate']
        price_raw = rrp + flat_fee  # RRP + $5.00
        price_raw = max(price_raw, CONFIG['minimumListingPrice'])
        final_price = math.ceil(price_raw) - 0.01 if CONFIG['charmPrice'] else round(price_raw, 2)
        final_price_str = f"{final_price:.2f}"
        profit_est = final_price * (1 - ebay_fee) - cost
        margin_pct = (profit_est / (final_price * (1 - ebay_fee))) * 100 if final_price > 0 else 0
        profit_est_str = f"{profit_est:.2f}"

        # Images
        img_urls = []
        for ic in img_cols:
            u = item.get(ic, '').strip()
            if u and u.startswith('http'):
                img_urls.append(u)
        if img_urls:
            hero = f"https://res.cloudinary.com/{cloudinary_cloud}/image/fetch/{watermark_layer}/{img_urls[0]}"
            pic_str = '|'.join([hero] + img_urls[1:])
        else:
            pic_str = ''

        # Category matching (first keyword match wins)
        search_text = f"{subsubcat} {subcat} {cat} {final_title}".lower()
        category_id = CATEGORY_MAP['default']
        for k, v in CATEGORY_MAP.items():
            if k != 'default' and k in search_text:
                category_id = v
                break

        # Hard overrides for edge cases
        if 'smartwatch' in search_text or 'fitbit' in search_text or 'apple watch' in search_text:
            category_id = '182068'
        elif 'bbq' in search_text or 'grill brush' in search_text:
            category_id = '177066'

        # Item specifics
        specs = extract_specs({
            'SKU': sku, 'Description': raw_desc,
            'Title': raw_title, 'Category': cat, 'Subcategory': subcat
        }, final_title)

        # Quantity
        raw_qty_str = re.sub(r'[^0-9]', '', str(item.get(qty_col, '0')))
        raw_qty = int(raw_qty_str) if raw_qty_str else 0
        list_qty = min(raw_qty if raw_qty > 0 else 1, CONFIG['maxListingQuantity'])

        # HTML Description
        clean_desc = re.sub(r'<img[^>]*dropshipzone[^>]*>', '', raw_desc, flags=re.I)
        clean_desc = re.sub(r'<img[^>]*logo\.png[^>]*>', '', clean_desc, flags=re.I)
        clean_desc = re.sub(r'<div>\s*<h2>Returns.*?</div>', '', clean_desc, flags=re.I | re.S).strip()
        if not clean_desc or len(clean_desc) < 20:
            clean_desc = f"<p>{re.sub(r'<[^>]+>', ' ', raw_desc).strip()}</p>"

        if is_store2:
            hero_card = ''
            if img_urls:
                hero_card = (
                    f'<div style="background:#FCF8F7;border:1px solid #F2E7E5;border-radius:10px;'
                    f'padding:22px;margin-bottom:24px;text-align:center;">'
                    f'<img src="{img_urls[0]}" alt="{final_title}" '
                    f'style="max-width:100%;max-height:480px;width:auto;height:auto;border-radius:8px;" />'
                    f'</div>'
                )

            html_desc = (
                f'<div style="max-width:880px;margin:0 auto;background-color:#FFFFFF;border-radius:16px;'
                f'padding:30px;box-sizing:border-box;border:1px solid #EFE4E2;'
                f'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;color:#4E5361;">'
                f'<div style="background-color:#FCF8F7;border-radius:12px;padding:40px 24px 34px 24px;'
                f'text-align:center;margin-bottom:26px;border:1px solid #F0E4E2;">'
                f'<a href="https://www.ebay.com.au/str/augoodvantage" target="_blank" '
                f'style="display:inline-block;padding:6px 20px;background-color:#FFFFFF;border-radius:20px;'
                f'font-size:11px;font-weight:700;letter-spacing:2px;color:#4E5361;text-transform:uppercase;'
                f'margin-bottom:14px;border:1px solid #E5A19C;text-decoration:none;">'
                f'OFFICIAL EBAY STORE &nbsp;›</a>'
                f'<h1 style="font-size:40px;color:#4E5361;margin:0 0 6px 0;font-weight:700;letter-spacing:-0.5px;">'
                f'<a href="https://www.ebay.com.au/str/augoodvantage" target="_blank" '
                f'style="color:#4E5361;text-decoration:none;">au<span style="color:#E5A19C;">good</span>vantage</a></h1>'
                f'<div style="font-size:13px;font-weight:700;letter-spacing:2.5px;color:#4E5361;text-transform:uppercase;margin-bottom:8px;">'
                f'SMART CHOICES. <span style="color:#E5A19C;">BETTER DEALS.</span> GOOD VANTAGE.</div>'
                f'<div style="width:120px;height:2px;background-color:#E5A19C;margin:0 auto 10px auto;border-radius:2px;"></div>'
                f'<p style="font-size:13px;color:#7B8292;margin:0 auto;max-width:520px;line-height:1.5;">'
                f'Helping you live well for less with feel-good finds and everyday essentials.</p></div>'
                f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:26px;">'
                f'<div style="display:flex;align-items:center;background:#FCF8F7;border:1px solid #F2E7E5;border-radius:10px;padding:14px 16px;">'
                f'<div style="width:38px;height:38px;background-color:#E5A19C;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:16px;margin-right:12px;flex-shrink:0;">🏷️</div>'
                f'<div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;letter-spacing:0.5px;">Smart Savings</div><div style="font-size:12px;color:#7B8292;">Quality products at great prices</div></div></div>'
                f'<div style="display:flex;align-items:center;background:#FCF8F7;border:1px solid #F2E7E5;border-radius:10px;padding:14px 16px;">'
                f'<div style="width:38px;height:38px;background-color:#E5A19C;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:16px;margin-right:12px;flex-shrink:0;">🤍</div>'
                f'<div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;letter-spacing:0.5px;">Curated with Care</div><div style="font-size:12px;color:#7B8292;">Handpicked for your lifestyle</div></div></div>'
                f'<div style="display:flex;align-items:center;background:#FCF8F7;border:1px solid #F2E7E5;border-radius:10px;padding:14px 16px;">'
                f'<div style="width:38px;height:38px;background-color:#E5A19C;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:16px;margin-right:12px;flex-shrink:0;">🛍️</div>'
                f'<div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;letter-spacing:0.5px;">Shop with Confidence</div><div style="font-size:12px;color:#7B8292;">100% Australian Stock &amp; Fast Dispatch</div></div></div></div>'
                f'<div style="background:#FFFFFF;border:1px solid #EFE4E2;border-radius:10px;padding:24px 28px;margin-bottom:24px;">'
                f'<h2 style="font-size:22px;color:#4E5361;margin:0 0 10px 0;line-height:1.35;font-weight:600;">{final_title}</h2>'
                f'<div style="font-size:12px;color:#8C92A0;">Item Code: <span style="color:#4E5361;font-weight:600;">AGV-{sku}</span> &nbsp;•&nbsp; Condition: <span style="color:#E5A19C;font-weight:700;">Brand New In Box</span> &nbsp;•&nbsp; Stock: <span style="color:#4E5361;font-weight:600;">Domestic AU Warehouse</span></div></div>'
                f'{hero_card}'
                f'<div style="background:#FFFFFF;border:1px solid #EFE4E2;border-radius:10px;padding:30px 32px;margin-bottom:24px;line-height:1.75;color:#525968;font-size:14px;">'
                f'<h3 style="font-size:17px;color:#4E5361;margin:0 0 14px 0;font-weight:600;border-bottom:2px solid #FAF0EE;padding-bottom:8px;">Product Overview</h3>'
                f'{clean_desc}</div>'
                f'<div style="background:#FCF8F7;border:1px solid #F0E4E2;border-radius:10px;padding:26px 28px;margin-bottom:24px;">'
                f'<h3 style="font-size:13px;color:#E5A19C;margin:0 0 18px 0;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;text-align:center;">The AuGoodVantage Difference</h3>'
                f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;text-align:center;">'
                f'<div><div style="font-size:20px;margin-bottom:4px;">🌿</div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;">Everyday Essentials</div><div style="font-size:11px;color:#7B8292;margin-top:2px;">From home to lifestyle, we\'ve got you covered.</div></div>'
                f'<div><div style="font-size:20px;margin-bottom:4px;">🏠</div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;">Lifestyle for Less</div><div style="font-size:11px;color:#7B8292;margin-top:2px;">Look good, feel good, without overspending.</div></div>'
                f'<div><div style="font-size:20px;margin-bottom:4px;">🎁</div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;">Made for You</div><div style="font-size:11px;color:#7B8292;margin-top:2px;">Thoughtful finds that add value to your day.</div></div>'
                f'<div><div style="font-size:20px;margin-bottom:4px;">😊</div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;">Good Vibes Only</div><div style="font-size:11px;color:#7B8292;margin-top:2px;">Shopping should be easy and enjoyable.</div></div></div></div>'
                f'<div style="background-color:#3E4657;border-radius:10px;padding:28px 32px;margin-bottom:24px;color:#FFFFFF;">'
                f'<h3 style="font-size:13px;color:#E5A19C;margin:0 0 18px 0;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;">Store Commitment &amp; Customer Care</h3>'
                f'<div style="margin-bottom:16px;"><h4 style="font-size:14px;color:#FFFFFF;margin:0 0 4px 0;font-weight:600;">🇦🇺 100% Australian Stock — Dispatched in 24 Hours</h4>'
                f'<p style="font-size:13px;line-height:1.6;color:#CBD5E1;margin:0;">All items are held locally in domestic Australian fulfillment centers and dispatched within 24 hours of payment clearance (Mon–Fri). Estimated delivery is <strong>2 to 6 business days</strong> nationwide with full tracking provided.</p></div>'
                f'<div style="margin-bottom:16px;"><h4 style="font-size:14px;color:#FFFFFF;margin:0 0 4px 0;font-weight:600;">🛡️ 30-Day Returns &amp; Australian Consumer Law Guarantee</h4>'
                f'<p style="font-size:13px;line-height:1.6;color:#CBD5E1;margin:0;">Shop with total confidence. Products received faulty, damaged, or not as described are eligible for a prompt replacement or refund in full accordance with Australian Consumer Law (ACL).</p></div>'
                f'<div><h4 style="font-size:14px;color:#FFFFFF;margin:0 0 4px 0;font-weight:600;">💬 Dedicated Australian Support</h4>'
                f'<p style="font-size:13px;line-height:1.6;color:#CBD5E1;margin:0;">Have questions or need assistance? Reach out anytime via eBay Messages — our Australian support team responds promptly within 24 hours.</p></div></div>'
                f'<div style="text-align:center;padding:14px 10px 4px 10px;font-size:12px;color:#7B8292;">'
                f'<p style="margin:0 0 4px 0;font-size:15px;color:#4E5361;font-weight:700;letter-spacing:1px;text-transform:uppercase;">'
                f'<a href="https://www.ebay.com.au/str/augoodvantage" target="_blank" style="color:#4E5361;text-decoration:none;">au<span style="color:#E5A19C;">good</span>vantage Store</a></p>'
                f'<p style="margin:0 0 14px 0;color:#7B8292;">Smart Choices. Better Deals. Good Vantage. &nbsp;•&nbsp; Official eBay Australia Store</p>'
                f'<a href="https://www.ebay.com.au/str/augoodvantage" target="_blank" style="display:inline-block;padding:10px 28px;background-color:#E5A19C;color:#FFFFFF;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;border-radius:25px;text-decoration:none;box-shadow:0 4px 14px rgba(229,161,156,0.4);">'
                f'Visit Our eBay Store &nbsp;›</a></div></div>'
            )
        else:
            hero_img_tag = ''
            if img_urls:
                hero_img_tag = (f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;'
                                f'border-radius:8px;padding:20px;margin-bottom:24px;text-align:center;">'
                                f'<img src="{img_urls[0]}" alt="{final_title}" '
                                f'style="max-width:100%;max-height:480px;width:auto;height:auto;border-radius:6px;" />'
                                f'</div>')

            html_desc = (
                f'<div style="max-width:880px;margin:0 auto;background-color:#F7F5F0;border-radius:12px;'
                f'padding:28px;box-sizing:border-box;border:1px solid #E2DED4;'
                f'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">'
                f'<div style="background-color:#F2EFE8;border-radius:10px;padding:42px 20px 36px 20px;'
                f'text-align:center;margin-bottom:28px;border:1px solid #E5E0D5;">'
                f'<a href="https://www.ebay.com.au/str/pivotliving" target="_blank" '
                f'style="display:inline-block;padding:6px 20px;background-color:#FAF8F5;border-radius:20px;'
                f'font-size:11px;font-weight:700;letter-spacing:2px;color:#2C3135;'
                f'text-transform:uppercase;margin-bottom:14px;border:1px solid #E6D7C3;text-decoration:none;">'
                f'OFFICIAL EBAY STORE &nbsp;›</a>'
                f'<h1 style="font-size:38px;color:#2C3135;margin:0 0 4px 0;font-weight:600;">'
                f'<a href="https://www.ebay.com.au/str/pivotliving" target="_blank" '
                f'style="color:#2C3135;text-decoration:none;">PivotLiving</a></h1>'
                f'<div style="width:240px;height:1.5px;background-color:#2C3135;margin:0 auto 12px auto;"></div>'
                f'<p style="font-size:14px;color:#4A5056;margin:0;letter-spacing:3px;'
                f'text-transform:uppercase;font-weight:500;">Modern Lifestyle Goods</p></div>'
                f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;'
                f'padding:14px 22px;margin-bottom:28px;font-size:12px;color:#525B62;'
                f'letter-spacing:0.5px;text-transform:uppercase;font-weight:600;display:flex;flex-wrap:wrap;">'
                f'<div>100% Australian Stock</div><div>&nbsp;|&nbsp;</div>'
                f'<div>Ships in 24 Hours</div><div>&nbsp;|&nbsp;</div>'
                f'<div>2–6 Days Transit</div><div>&nbsp;|&nbsp;</div>'
                f'<div>High Positive Feedback</div></div>'
                f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;'
                f'padding:26px 30px;margin-bottom:28px;">'
                f'<h2 style="font-size:23px;color:#2C3135;margin:0 0 10px 0;">{final_title}</h2>'
                f'<div style="font-size:12px;color:#78828A;">Item Code: '
                f'<span style="color:#2C3135;font-weight:600;">DSZ-{sku}</span></div></div>'
                f'{hero_img_tag}'
                f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;'
                f'padding:32px 34px;margin-bottom:28px;line-height:1.75;color:#383F45;font-size:14px;">'
                f'{clean_desc}</div>'
                f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;'
                f'padding:30px 34px;margin-bottom:28px;">'
                f'<h3 style="font-size:13px;color:#78828A;margin:0 0 18px 0;text-transform:uppercase;">'
                f'Store Commitment &amp; Customer Care</h3>'
                f'<h4 style="font-size:14px;color:#2C3135;">100% Australian Stock — Ships in 24 Hours</h4>'
                f'<p style="font-size:13px;color:#525B62;">All items are held locally in domestic Australian '
                f'fulfillment centers and dispatched within 24 hours of payment clearance (Mon–Fri). '
                f'Estimated delivery: <strong>2 to 6 business days</strong> nationwide with tracking.</p>'
                f'<h4 style="font-size:14px;color:#2C3135;">Dedicated Customer Service</h4>'
                f'<p style="font-size:13px;color:#525B62;">Reach out via eBay Messages — our local team '
                f'will promptly assist you before and after your purchase.</p></div></div>'
            )

        ebay_row = {
            '*Action':                    'Add',
            '*Title':                     final_title,
            '*Category':                  category_id,
            'CustomLabel':                dsz_sku,
            '*ConditionID':               '1000',
            '*StartPrice':                final_price_str,
            '*Quantity':                  str(list_qty),
            '*Format':                    'FixedPrice',
            '*Duration':                  'GTC',
            'ShippingType':               'Free',
            'ShippingService-1:Option':   'AU_StandardDelivery',
            'ShippingService-1:Cost':     '0.00',
            'DispatchTimeMax':            '1',
            'Country':                    'AU',
            '*Location':                  'Australia',
            'PicURL':                     pic_str,
            'Description':                html_desc,
        }
        ebay_row.update(specs)
        ebay_rows.append(ebay_row)

        if index < 10:
            print(f"[#{index + 1}] {sku} | Cat: {category_id} | Title: {final_title} "
                  f"({len(final_title)}ch) | Sell: ${final_price_str} | "
                  f"Profit: ${profit_est_str} ({margin_pct:.1f}%)")

    # ── Save Outputs ──────────────────────────────────────────────────────────
    if is_store2:
        output_path_workspace = "c:/Users/andre/Ebay/pipeline/output_ebay_upload_store2.csv"
        output_path_downloads = f"C:/Users/andre/Downloads/output_ebay_upload_store2_{feed_key}_new_batch.csv"
        output_path_root = "c:/Users/andre/Ebay/output_ebay_upload_store2.csv"
        output_path_downloads_all = f"C:/Users/andre/Downloads/output_ebay_upload_store2_all.csv"
    else:
        output_path_workspace = "c:/Users/andre/Ebay/pipeline/output_ebay_upload.csv"
        output_path_downloads = f"C:/Users/andre/Downloads/output_ebay_upload_{feed_key}.csv"
        output_path_root = "c:/Users/andre/Ebay/output_ebay_upload.csv"
        output_path_downloads_all = None

    if ebay_rows or (is_store2 and os.path.exists(output_path_root)):
        combined_rows = []
        seen_skus_in_out = set()
        if is_store2 and os.path.exists(output_path_root):
            with open(output_path_root, mode="r", encoding="utf-8-sig", errors="ignore") as rf:
                r_reader = csv.DictReader(rf)
                for row in r_reader:
                    cl = row.get('CustomLabel', '').strip()
                    if cl and cl not in seen_skus_in_out:
                        seen_skus_in_out.add(cl)
                        # Ensure existing Store 2 titles end in AU Fast Post rather than AU Stock
                        row['*Title'] = format_title(row.get('*Title', ''), is_store2)
                        combined_rows.append(row)
            
            for er in ebay_rows:
                cl = er.get('CustomLabel', '').strip()
                if cl and cl not in seen_skus_in_out:
                    seen_skus_in_out.add(cl)
                    combined_rows.append(er)
        else:
            combined_rows = list(ebay_rows)

        headers = list(combined_rows[0].keys())
        
        # Write merged master catalog
        for out_path in [output_path_workspace, output_path_root]:
            with open(out_path, mode="w", encoding="utf-8-sig", newline="") as wf:
                writer = csv.DictWriter(wf, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(combined_rows)
        
        if output_path_downloads_all:
            with open(output_path_downloads_all, mode="w", encoding="utf-8-sig", newline="") as wf:
                writer = csv.DictWriter(wf, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(combined_rows)

        # Also write the newly processed batch file separately for clean upload
        if ebay_rows:
            with open(output_path_downloads, mode="w", encoding="utf-8-sig", newline="") as wf:
                writer = csv.DictWriter(wf, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(ebay_rows)

    print("\n=======================================================")
    print(f"✅ Successfully Processed {len(ebay_rows)} New Winning Dropshipzone Products for {store_name}!")
    if is_store2:
        print(f"📊 Total Combined Listings in Store 2 Master Catalog: {len(combined_rows)} listings.")
    print(f"⏭️ Skipped {skipped_count} products (already active on eBay).")
    print(f"🚫 Filtered {prohibited_count} prohibited/restricted products.")
    print(f"📁 Workspace Output: {output_path_workspace}")
    if is_store2 and output_path_downloads_all:
        print(f"📁 Downloads Full Catalog: {output_path_downloads_all}")
    print(f"📁 Downloads New Batch Output: {output_path_downloads}")
    print(f"📁 Root Output: {output_path_root}")
    print("=======================================================\n")

    # ── Update delta snapshot ─────────────────────────────────────────────────
    all_feed_skus = set(r.get(sku_col, '').strip() for r in parsed_items if r.get(sku_col, '').strip())
    if snapshot_file.exists():
        all_feed_skus |= set(snapshot_file.read_text(encoding='utf-8').splitlines())
    snapshot_file.write_text('\n'.join(sorted(all_feed_skus)), encoding='utf-8')
    print(f"💾 Delta snapshot updated: {len(all_feed_skus)} total SKUs → {snapshot_file}")


if __name__ == "__main__":
    main()
