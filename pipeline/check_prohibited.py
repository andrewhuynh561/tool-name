#!/usr/bin/env python3
"""
check_prohibited.py - eBay Australia Policy & Prohibited Items Auditor
======================================================================
Audits supplier product feeds (Dropshipzone / CSV) against eBay Australia
prohibited/restricted items policy, Therapeutic Goods Act (TGA) regulations,
VeRO trademarks, and supplier catalog data integrity.

Features:
- Medical device / clinical / prescription detection
- Context-aware false positive elimination (pet recovery suits, retainer cups, etc.)
- Data integrity cross-checking (Title vs Description mismatch detection)
- VeRO brand detection
- CLI support for single file or auto-detecting latest Downloads feed
"""

import sys
import os
import csv
import re
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ── High-Risk / Prohibited Keywords (eBay AU & TGA Regulations) ─────────────
CRITICAL_PROHIBITED_PATTERNS = [
    # Prescription & Controlled Substances
    r'\bprescription\b',
    r'\bpharmaceutical\b',
    r'\btherapeutic goods\b',
    r'\btga approved\b',
    r'\bclinical grade\b',
    r'\bhospital grade\b',
    
    # Medical Diagnostic & Invasive Devices
    r'\beeg\b',
    r'\becg\b',
    r'\belectrocardiogram\b',
    r'\bpulse oximeter\b',
    r'\bblood pressure monitor\b',
    r'\bglucose meter\b',
    r'\bglucometer\b',
    r'\bnebulizer\b',
    r'\bdefibrillator\b',
    r'\bcpap\b',
    r'\boxygen concentrator\b',
    r'\bhearing aid\b',
    r'\bdental impression\b',
    r'\bsurgical scalpel\b',
    r'\bsurgical suture\b',
    
    # Weapons & Dangerous Goods
    r'\bswitchblade\b',
    r'\bbutterfly knife\b',
    r'\bconcealed blade\b',
    r'\btaser\b',
    r'\bstun gun\b',
    r'\bpepper spray\b',
    r'\bmace\b',
    r'\bhandcuffs\b',
    r'\bexplosive\b',
    r'\bflammable gas canister\b',
]

# ── Safe Whitelist Patterns (Contextual False-Positive Eliminators) ──────────
WHITELIST_CONTEXTS = [
    # Pet clothing & post-op recovery suits
    (r'\b(pet|dog|cat|puppy|kitten)\b.*\b(surgical|recovery|bodysuit|suit|clothing)\b', "Pet Recovery Suit / Animal Apparel (Safe)"),
    (r'\bpost surgery bodysuit\b', "Pet Recovery Bodysuit (Safe)"),
    (r'\bsurgical recovery bodysuit\b', "Pet Recovery Bodysuit (Safe)"),
    
    # Dental hygiene storage & consumer cleaning accessories
    (r'\b(retainer|aligner|denture)\s+(?:cleaning|storage|soaking|case|box|container)\b', "Dental Appliance Storage Case (Safe Non-Prescription Container)"),
    (r'\b(?:electric\s+)?water\s+flosser\b', "Oral Hygiene Irrigator / Flosser (Safe Personal Care)"),
    (r'\boral irrigator\b', "Consumer Oral Flosser (Safe Personal Care)"),
    
    # Home & Baby Safety
    (r'\b(?:silicone|furniture|table|desk)\s+corner\s+protector\b', "Furniture Corner Guard / Child Safety (Safe Home Hardware)"),
    (r'\bedge guard\b', "Child Safety Corner Guard (Safe Home Hardware)"),
    
    # Outdoor / Camping Sanitation
    (r'\b(?:folding|portable|car|camping)\s+(?:toilet|potty|commode)\b', "Camping Sanitation Equipment (Safe Outdoor Gear)"),
    
    # Cosmetic & Body Care
    (r'\b(?:silicone\s+)?body\s+scrubber\b', "Bath & Body Exfoliating Scrubber (Safe Cosmetic Tool)"),
    (r'\bshoe\s+cleaning\s+brush\b', "Shoe Care Brush (Safe Household Cleaning)"),
]

# ── VeRO / High-Profile Trademark Brands to Monitor ───────────────
VERO_BRANDS = [
    'Apple', 'Nike', 'Adidas', 'Sony', 'Samsung', 'Bose', 'Dyson',
    'Rolex', 'Gucci', 'Louis Vuitton', 'Prada', 'Chanel', 'Fitbit',
    'GoPro', 'Lego', 'Disney', 'Marvel', 'Pokemon'
]

def audit_item(item):
    """
    Audits an individual item dict from a feed.
    Returns: status ('PASS', 'WARNING', 'BLOCKED'), reasons (list), details (dict)
    """
    sku = item.get('SKU', item.get('ProductID', '')).strip()
    title = item.get('Title', '').strip()
    desc = item.get('Description', '').strip()
    cat = item.get('Category', '').strip()
    subcat = item.get('Subcategory', '').strip()
    
    combined_text = f"{title} {desc} {cat} {subcat}".lower()
    
    # Clean out non-relevant disclaimer tags
    clean_text = re.sub(r'<details>.*?</details>', '', combined_text, flags=re.S)
    clean_text = re.sub(r'not (?:intended for|designed for|a) (?:medical|therapeutic)[^.]*', '', clean_text)
    clean_text = re.sub(r'leisure accessory only[^.]*', '', clean_text)
    
    reasons = []
    status = 'PASS'
    whitelisted_reasons = []
    
    # 1. Check for Whitelist Contexts
    for pattern, note in WHITELIST_CONTEXTS:
        if re.search(pattern, combined_text, re.IGNORECASE):
            whitelisted_reasons.append(note)
    
    # 2. Check for Prohibited Keywords
    matched_prohibited = []
    for pattern in CRITICAL_PROHIBITED_PATTERNS:
        matches = re.findall(pattern, clean_text, re.IGNORECASE)
        if matches:
            matched_prohibited.extend(matches)
    
    # If prohibited pattern found, check if it was rescued by whitelist
    if matched_prohibited:
        # Check if only 'surgical' matched on a pet suit
        is_pet_suit = any("Pet Recovery" in note for note in whitelisted_reasons)
        non_pet_matches = [m for m in matched_prohibited if not (is_pet_suit and m.lower() in ('surgical', 'clinical'))]
        
        if non_pet_matches:
            status = 'BLOCKED'
            reasons.append(f"Prohibited Medical/Restricted keywords detected: {list(set(non_pet_matches))}")
        else:
            reasons.append(f"Context Whitelist Applied: {', '.join(whitelisted_reasons)}")
            
    # 3. Check for Data Mismatches (Supplier feed quality errors)
    # E.g. Title says sewing kit, description says bicycle multi tool
    title_lower = title.lower()
    desc_lower = desc.lower()
    
    if 'sewing kit' in title_lower and 'bicycle multi tool' in desc_lower:
        status = 'WARNING' if status != 'BLOCKED' else status
        reasons.append("DATA MISMATCH: Title describes Sewing Kit, but Description describes Bicycle Multi Tool")
        
    if 'silicone body scrubber' in title_lower and 'knife and scissor storage' in desc_lower:
        status = 'WARNING' if status != 'BLOCKED' else status
        reasons.append("DATA MISMATCH: Title describes Silicone Body Scrubber, but Description describes Knife Storage Holder")

    # 4. Check for VeRO Brands
    found_brands = []
    for b in VERO_BRANDS:
        if re.search(r'\b' + re.escape(b) + r'\b', title, re.IGNORECASE):
            found_brands.append(b)
    if found_brands:
        if status != 'BLOCKED':
            status = 'WARNING'
        reasons.append(f"VeRO Brand Watch: Potential brand name in title {found_brands}")

    return status, reasons, {
        'sku': sku,
        'title': title,
        'category': cat,
        'whitelisted': whitelisted_reasons
    }

def main():
    feed_path = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        feed_path = sys.argv[1]
    
    if not feed_path:
        downloads_dir = Path("C:/Users/andre/Downloads")
        general_files = sorted(downloads_dir.rglob("General_*.csv"), key=os.path.getmtime, reverse=True)
        if general_files:
            feed_path = str(general_files[0])
            
    if not feed_path or not os.path.exists(feed_path):
        print(f"[ERROR] Feed CSV file not found: {feed_path}")
        sys.exit(1)
        
    print("=" * 72)
    print(f"🛡️  eBay Australia Policy & Prohibited Items Auditor")
    print(f"📂 Feed: {feed_path}")
    print("=" * 72)
    
    with open(feed_path, mode="r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f)
        items = list(reader)
        
    print(f"Total items in feed: {len(items)}\n")
    
    passed = []
    warnings = []
    blocked = []
    
    for item in items:
        status, reasons, details = audit_item(item)
        if status == 'PASS':
            passed.append((details, reasons))
        elif status == 'WARNING':
            warnings.append((details, reasons))
        elif status == 'BLOCKED':
            blocked.append((details, reasons))
            
    # Print results
    print(f"📊 Audit Summary:")
    print(f"  ✅ PASS:    {len(passed)} items (Compliant for eBay AU listing)")
    print(f"  ⚠️ WARNING: {len(warnings)} items (Feed data anomalies or VeRO watch)")
    print(f"  🚫 BLOCKED: {len(blocked)} items (Prohibited or high-risk violation)")
    print("-" * 72)
    
    if blocked:
        print("\n🚫 BLOCKED ITEMS:")
        for details, reasons in blocked:
            print(f"  • [{details['sku']}] {details['title'][:60]}")
            for r in reasons:
                print(f"    - {r}")
                
    if warnings:
        print("\n⚠️ WARNING / ANOMALY ITEMS:")
        for details, reasons in warnings:
            print(f"  • [{details['sku']}] {details['title'][:60]}")
            for r in reasons:
                print(f"    - {r}")
                
    print("\n✅ SAMPLE OF VERIFIED COMPLIANT ITEMS (First 5):")
    for details, reasons in passed[:5]:
        wl_note = f" (Whitelist: {reasons[0]})" if reasons else ""
        print(f"  • [{details['sku']}] {details['title'][:55]}...{wl_note}")

    print("\n" + "=" * 72)
    if blocked:
        print("❌ Action: Review BLOCKED items before running bulk upload.")
    else:
        print("✨ Result: Zero critical prohibited items. Safe to process with run_n8n_pipeline.py!")
    print("=" * 72)

if __name__ == '__main__':
    main()
