import csv
import re
import os
import html

def clean_html_description(raw_desc, title):
    if not raw_desc:
        raw_desc = ""
    # Strip tracking pixels & vendor artifacts
    cleaned = raw_desc
    cleaned = re.sub(r'<img[^>]*dropshipzone[^>]*>', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'<img[^>]*logo\.png[^>]*>', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'<h3>\s*Returns,\s*Refunds,?\s*and\s*Replacements[\s\S]*?(?=<h3>|<div|$)', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'<div>\s*<h2>Returns,\s*Refunds,?\s*and\s*Replacements</h2>[\s\S]*?</div>', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'<p>\s*Note:\s*This product is shipped from outside Australia[\s\S]*?<\/p>', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'NOTE:\s*PO BOX address is not supported[\s\S]*?(?=<br|<\/p|$)', '', cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()

    if not cleaned or len(cleaned) < 20:
        plain = re.sub(r'<[^>]+>', ' ', raw_desc)
        plain = re.sub(r'\s{2,}', ' ', plain).strip()
        if plain and len(plain) >= 20:
            cleaned = f'<p style="margin:0 0 16px 0;font-size:14px;color:#525968;line-height:1.75;">{plain}</p>'
        else:
            cleaned = (
                f'<p style="margin:0 0 16px 0;font-size:14px;color:#525968;line-height:1.75;">'
                f'Elevate your day-to-day comfort and lifestyle with this versatile, high-grade essential. '
                f'Carefully selected by <strong>AuGoodVantage</strong> for durability, aesthetic design, and everyday practicality, '
                f'this product is designed to give you better value and effortless enjoyment.'
                f'</p>'
            )
    return cleaned

def generate_augoodvantage_html(title, sku, hero_img, clean_desc):
    title_escaped = html.escape(title)
    item_code_str = f"AGV-{sku}" if not sku.startswith("AGV-") else sku
    
    hero_card = ''
    if hero_img:
        hero_card = (
            f'<div style="background:#FCF8F7;border:1px solid #F2E7E5;border-radius:10px;padding:22px;margin-bottom:24px;text-align:center;">'
            f'<img src="{hero_img}" alt="{title_escaped}" style="max-width:100%;max-height:480px;width:auto;height:auto;border-radius:8px;" />'
            f'</div>'
        )

    html_desc = (
        f'<div style="max-width:880px;margin:0 auto;background-color:#FFFFFF;border-radius:16px;padding:30px;box-sizing:border-box;'
        f'border:1px solid #EFE4E2;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;color:#4E5361;">'
        f'<div style="background-color:#FCF8F7;border-radius:12px;padding:40px 24px 34px 24px;text-align:center;margin-bottom:26px;border:1px solid #F0E4E2;">'
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
        f'<div><div style="font-size:12px;font-weight:700;color:#4E5361;text-transform:uppercase;letter-spacing:0.5px;">Shop with Confidence</div><div style="font-size:12px;color:#7B8292;">100% Australian Stock &amp; 5–10 Business Days Delivery</div></div></div></div>'
        f'<div style="background:#FFFFFF;border:1px solid #EFE4E2;border-radius:10px;padding:24px 28px;margin-bottom:24px;">'
        f'<h2 style="font-size:22px;color:#4E5361;margin:0 0 10px 0;line-height:1.35;font-weight:600;">{title_escaped}</h2>'
        f'<div style="font-size:12px;color:#8C92A0;">Item Code: <span style="color:#4E5361;font-weight:600;">{item_code_str}</span> &nbsp;•&nbsp; Condition: <span style="color:#E5A19C;font-weight:700;">Brand New In Box</span> &nbsp;•&nbsp; Stock: <span style="color:#4E5361;font-weight:600;">Domestic AU Warehouse</span></div></div>'
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
        f'<div style="margin-bottom:16px;"><h4 style="font-size:14px;color:#FFFFFF;margin:0 0 4px 0;font-weight:600;">🇦🇺 100% Australian Stock — 5 to 10 Business Days Delivery</h4>'
        f'<p style="font-size:13px;line-height:1.6;color:#CBD5E1;margin:0;">All items are held locally in domestic Australian fulfillment centers and dispatched promptly with full online tracking provided. Estimated delivery timeframe is <strong>5 to 10 business days</strong> nationwide.</p></div>'
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
    return html_desc

def main():
    feed_files = [
        'pipeline/General_20260903T223710.csv',
        'C:/Users/andre/Downloads/General_20260909T214257.csv',
        'output_ebay_upload_store2.csv'
    ]
    
    feed_db_by_sku = {}
    feed_db_by_title = {}

    for fpath in feed_files:
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sku = r.get('SKU') or r.get('CustomLabel') or ''
                    sku = sku.strip().upper().replace('AGV-', '').replace('DSZ-', '')
                    if sku and sku not in feed_db_by_sku:
                        feed_db_by_sku[sku] = r
                    t = (r.get('Title') or r.get('*Title') or '').strip().lower()
                    if t and t not in feed_db_by_title:
                        feed_db_by_title[t] = r

    print(f"Loaded {len(feed_db_by_sku)} feed products across sources.")

    active_report = 'C:/Users/andre/Downloads/eBay-all-active-listings-report-2026-09-11-13327147699.csv'
    with open(active_report, 'r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.DictReader(f)
        active_rows = list(reader)

    # Deduplicate active listings by Item number
    items_to_revise = {}
    for r in active_rows:
        it = r.get('Item number', '').strip()
        if it and it not in items_to_revise:
            items_to_revise[it] = r

    print(f"Found {len(items_to_revise)} unique active eBay listings to revise for AuGoodVantage.")

    output_file = 'output_ebay_revise_store2.csv'
    matched_count = 0
    fallback_count = 0

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['*Action', 'ItemID', 'Description'])

        for item_id, row in items_to_revise.items():
            sku = row.get('Custom label (SKU)', '').strip()
            cleaned_sku = sku.upper().replace('AGV-', '').replace('DSZ-', '').strip()
            title = row.get('Title', '').strip()

            feed_item = feed_db_by_sku.get(cleaned_sku) or feed_db_by_sku.get(sku.upper())
            if not feed_item and title.lower() in feed_db_by_title:
                feed_item = feed_db_by_title[title.lower()]
            if not feed_item:
                t_clean = title.replace('AU Fast Post', '').replace('AU Stock', '').strip().lower()
                for ft, frow in feed_db_by_title.items():
                    if t_clean in ft or ft in t_clean or (len(t_clean) > 20 and t_clean[:25] in ft):
                        feed_item = frow
                        break

            if feed_item:
                matched_count += 1
                raw_desc = feed_item.get('Description', '')
                feed_title = feed_item.get('Title') or feed_item.get('*Title') or title
                hero_img = (feed_item.get('Image 1') or feed_item.get('PicURL', '') or '').split('|')[0].strip()
            else:
                fallback_count += 1
                raw_desc = ""
                feed_title = title
                hero_img = ""

            clean_desc = clean_html_description(raw_desc, feed_title)
            html_desc = generate_augoodvantage_html(
                title=title,
                sku=sku if sku else item_id,
                hero_img=hero_img,
                clean_desc=clean_desc
            )

            writer.writerow(['Revise', item_id, html_desc])

    print(f"\n[DONE] Successfully generated {len(items_to_revise)} rows in {output_file}.")
    print(f"Matched with catalog data: {matched_count}")
    print(f"Clean fallback descriptions: {fallback_count}")

if __name__ == '__main__':
    main()
