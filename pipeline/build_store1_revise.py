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
    cleaned = cleaned.strip()

    if not cleaned or len(cleaned) < 20:
        plain = re.sub(r'<[^>]+>', ' ', raw_desc)
        plain = re.sub(r'\s{2,}', ' ', plain).strip()
        if plain and len(plain) >= 20:
            cleaned = f'<p style="margin:0 0 16px 0;font-size:15px;color:#2C3135;line-height:1.7;">{plain}</p>'
        else:
            cleaned = (
                f'<p style="margin:0 0 16px 0;font-size:15px;color:#2C3135;line-height:1.7;">'
                f'Introducing our premium <strong>{html.escape(title)}</strong>. '
                f'Engineered and selected for exceptional reliability, ease of use, and everyday performance. '
                f'Every item is backed by our PivotLiving satisfaction commitment and dispatched quickly from our domestic Australian warehouse.'
                f'</p>'
            )
    return cleaned

def generate_pivot_living_html(title, sku, hero_img, gallery_imgs, clean_desc):
    title_escaped = html.escape(title)
    
    # Hero image section
    main_image_section = ""
    if hero_img:
        main_image_section = (
            f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:20px;margin-bottom:24px;text-align:center;">'
            f'<img src="{hero_img}" alt="{title_escaped}" style="max-width:100%;max-height:480px;width:auto;height:auto;border-radius:6px;" />'
            f'</div>'
        )

    # Secondary gallery images
    extra_gallery_section = ""
    valid_gallery = [img for img in gallery_imgs if img and img.startswith('http') and img != hero_img]
    if len(valid_gallery) >= 2:
        extra_gallery_section = (
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:28px;">'
            f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:16px;text-align:center;">'
            f'<img src="{valid_gallery[0]}" alt="{title_escaped} Detail Photo 1" style="max-width:100%;max-height:380px;width:auto;height:auto;border-radius:6px;" />'
            f'</div>'
            f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:16px;text-align:center;">'
            f'<img src="{valid_gallery[1]}" alt="{title_escaped} Detail Photo 2" style="max-width:100%;max-height:380px;width:auto;height:auto;border-radius:6px;" />'
            f'</div>'
            f'</div>'
        )
    elif len(valid_gallery) == 1:
        extra_gallery_section = (
            f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:20px;margin-bottom:28px;text-align:center;">'
            f'<img src="{valid_gallery[0]}" alt="{title_escaped} Detail Photo 1" style="max-width:100%;max-height:450px;width:auto;height:auto;border-radius:6px;" />'
            f'</div>'
        )

    item_code_str = f"DSZ-{sku}" if not sku.startswith("DSZ-") else sku

    html_desc = (
        f'<div style="max-width:880px;margin:0 auto;background-color:#F7F5F0;border-radius:12px;padding:28px;box-sizing:border-box;border:1px solid #E2DED4;box-shadow:0 10px 35px rgba(0,0,0,0.04);font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">'
        f'<div style="background-color:#F2EFE8;background-image:radial-gradient(#E5E0D5 1px,transparent 1px);background-size:16px 16px;border-radius:10px;padding:42px 20px 36px 20px;text-align:center;margin-bottom:28px;border:1px solid #E5E0D5;position:relative;">'
        f'<a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="display:inline-block;padding:6px 20px;background-color:#FAF8F5;border-radius:20px;font-size:11px;font-weight:700;letter-spacing:2px;color:#2C3135;text-transform:uppercase;margin-bottom:14px;border:1px solid #E6D7C3;text-decoration:none;">OFFICIAL EBAY STORE &nbsp;&rsaquo;</a>'
        f'<h1 style="font-size:38px;color:#2C3135;margin:0 0 4px 0;font-weight:600;letter-spacing:-0.5px;">'
        f'<a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="color:#2C3135;text-decoration:none;">Piv<span style="position:relative;display:inline-block;">o<span style="position:absolute;left:48%;top:0;bottom:0;width:1.5px;background-color:#2C3135;transform:translateX(-50%);"></span></span>tLiving</a>'
        f'</h1>'
        f'<div style="width:240px;height:1.5px;background-color:#2C3135;margin:0 auto 12px auto;"></div>'
        f'<p style="font-size:14px;color:#4A5056;margin:0;letter-spacing:3px;text-transform:uppercase;font-weight:500;">Modern Lifestyle Goods</p>'
        f'<span style="position:absolute;right:24px;bottom:18px;color:#D8D2C6;font-size:16px;">&#10022;</span>'
        f'</div>'
        f'<div style="display:flex;flex-wrap:wrap;justify-content:space-between;background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:14px 22px;margin-bottom:28px;font-size:12px;color:#525B62;letter-spacing:0.5px;text-transform:uppercase;font-weight:600;">'
        f'<div>100% Australian Stock</div><div style="color:#D2CBC0;">|</div>'
        f'<div>Ships in 24 Hours</div><div style="color:#D2CBC0;">|</div>'
        f'<div>5&ndash;10 Business Days Transit</div><div style="color:#D2CBC0;">|</div>'
        f'<div>High Positive Feedback</div>'
        f'</div>'
        f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:26px 30px;margin-bottom:28px;">'
        f'<h2 style="font-size:23px;color:#2C3135;margin:0 0 10px 0;line-height:1.35;font-weight:600;letter-spacing:-0.3px;">{title_escaped}</h2>'
        f'<div style="font-size:12px;color:#78828A;font-weight:500;">Item Code: <span style="color:#2C3135;font-weight:600;">{item_code_str}</span> &nbsp;&bull;&nbsp; Condition: <span style="color:#2C3135;font-weight:600;">Brand New In Box</span></div>'
        f'</div>'
        f'{main_image_section}'
        f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:32px 34px;margin-bottom:28px;line-height:1.75;color:#383F45;font-size:14px;">'
        f'<h3 style="font-size:13px;color:#78828A;margin:0 0 16px 0;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Product Overview</h3>'
        f'{clean_desc}'
        f'</div>'
        f'{extra_gallery_section}'
        f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:30px 34px;margin-bottom:28px;">'
        f'<h3 style="font-size:13px;color:#78828A;margin:0 0 18px 0;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Item Specifications</h3>'
        f'<table style="width:100%;border-collapse:collapse;font-size:13px;color:#383F45;">'
        f'<tbody>'
        f'<tr style="border-bottom:1px solid #F0ECE4;"><td style="padding:12px 0;font-weight:600;color:#2C3135;width:35%;">Condition</td><td style="padding:12px 0;">Brand New In Original Packaging</td></tr>'
        f'<tr style="border-bottom:1px solid #F0ECE4;"><td style="padding:12px 0;font-weight:600;color:#2C3135;">Shipping Origin</td><td style="padding:12px 0;">Australia Domestic Fulfillment Center</td></tr>'
        f'<tr style="border-bottom:1px solid #F0ECE4;"><td style="padding:12px 0;font-weight:600;color:#2C3135;">Dispatch Handling</td><td style="padding:12px 0;">Dispatched within 24 Hours (Mon&ndash;Fri)</td></tr>'
        f'<tr style="border-bottom:1px solid #F0ECE4;"><td style="padding:12px 0;font-weight:600;color:#2C3135;">Estimated Delivery</td><td style="padding:12px 0;">5 to 10 Business Days with Online Tracking</td></tr>'
        f'<tr><td style="padding:12px 0;font-weight:600;color:#2C3135;">Customer Protection</td><td style="padding:12px 0;">Australian Consumer Law Guarantee &amp; Store Support</td></tr>'
        f'</tbody></table></div>'
        f'<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:30px 34px;margin-bottom:28px;">'
        f'<h3 style="font-size:13px;color:#78828A;margin:0 0 18px 0;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Store Commitment &amp; Customer Care</h3>'
        f'<div style="margin-bottom:22px;">'
        f'<h4 style="font-size:14px;color:#2C3135;margin:0 0 6px 0;font-weight:600;">100% Australian Stock &mdash; Ships in 24 Hours</h4>'
        f'<p style="font-size:13px;line-height:1.6;color:#525B62;margin:0;">All items are held locally in domestic Australian fulfillment centers and dispatched within 24 hours of payment clearance (Monday to Friday). Estimated delivery timeframe is <strong>5 to 10 business days</strong> nationwide, with online tracking provided immediately upon dispatch.</p>'
        f'</div>'
        f'<div style="margin-bottom:22px;">'
        f'<h4 style="font-size:14px;color:#2C3135;margin:0 0 6px 0;font-weight:600;">High Positive Feedback &amp; Quality Goods</h4>'
        f'<p style="font-size:13px;line-height:1.6;color:#525B62;margin:0;">At <strong>PivotLiving</strong>, we maintain a strong track record of high customer feedback by carefully selecting only reliable, high-grade products. We listen closely to buyer feedback, ensuring every item delivered to your door meets high standards of quality and dependability.</p>'
        f'</div>'
        f'<div>'
        f'<h4 style="font-size:14px;color:#2C3135;margin:0 0 6px 0;font-weight:600;">Dedicated Customer Service</h4>'
        f'<p style="font-size:13px;line-height:1.6;color:#525B62;margin:0;">We are committed to providing helpful, attentive service before and after your purchase. Have a question about this item or your order? Reach out anytime via eBay Messages and our local support team will promptly assist you.</p>'
        f'</div></div>'
        f'<div style="text-align:center;padding:18px 10px 5px 10px;font-size:12px;color:#8A949E;">'
        f'<p style="margin:0 0 6px 0;font-size:14px;color:#2C3135;font-weight:600;letter-spacing:1px;text-transform:uppercase;">'
        f'<a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="color:#2C3135;text-decoration:none;">PivotLiving Store</a>'
        f'</p>'
        f'<p style="margin:0 0 10px 0;">Modern Lifestyle Goods &nbsp;&bull;&nbsp; Official eBay Australia Store</p>'
        f'<a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="display:inline-block;padding:8px 22px;background-color:#2C3135;color:#F7F5F0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;border-radius:4px;text-decoration:none;">Visit Our eBay Store</a>'
        f'</div></div>'
    )
    return html_desc

def main():
    feed_files = [
        'pipeline/General_20260903T223710.csv',
        'C:/Users/andre/Downloads/General_20260909T214257.csv'
    ]
    
    feed_db_by_sku = {}
    feed_db_by_title = {}

    for fpath in feed_files:
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sku = r.get('SKU', '').strip().upper()
                    if sku and sku not in feed_db_by_sku:
                        feed_db_by_sku[sku] = r
                    t = r.get('Title', '').strip().lower()
                    if t and t not in feed_db_by_title:
                        feed_db_by_title[t] = r

    print(f"Loaded {len(feed_db_by_sku)} feed products.")

    active_report = 'C:/Users/andre/Downloads/eBay-all-active-listings-report-2026-09-11-12345105795.csv'
    with open(active_report, 'r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.DictReader(f)
        active_rows = list(reader)

    # Deduplicate active listings by Item number so each active listing has exactly 1 revise row
    items_to_revise = {}
    for r in active_rows:
        it = r.get('Item number', '').strip()
        if it and it not in items_to_revise:
            items_to_revise[it] = r

    print(f"Found {len(items_to_revise)} unique active eBay listings to revise.")

    output_file = 'output_ebay_revise_store1.csv'
    matched_count = 0
    fallback_count = 0

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['*Action', 'ItemID', 'Description'])

        for item_id, row in items_to_revise.items():
            sku = row.get('Custom label (SKU)', '').strip()
            cleaned_sku = sku.upper().replace('DSZ-', '').strip()
            title = row.get('Title', '').strip()

            feed_item = feed_db_by_sku.get(cleaned_sku) or feed_db_by_sku.get(sku.upper())
            if not feed_item and title.lower() in feed_db_by_title:
                feed_item = feed_db_by_title[title.lower()]
            if not feed_item:
                # check partial title match
                t_clean = title.replace('AU Stock', '').strip().lower()
                for ft, frow in feed_db_by_title.items():
                    if t_clean in ft or ft in t_clean or (len(t_clean) > 20 and t_clean[:25] in ft):
                        feed_item = frow
                        break

            if feed_item:
                matched_count += 1
                raw_desc = feed_item.get('Description', '')
                feed_title = feed_item.get('Title', '') or title
                hero_img = (feed_item.get('Image 1', '') or '').strip()
                gallery_imgs = [
                    (feed_item.get('Image 2', '') or '').strip(),
                    (feed_item.get('Image 3', '') or '').strip(),
                ]
            else:
                fallback_count += 1
                raw_desc = ""
                feed_title = title
                hero_img = ""
                gallery_imgs = []

            clean_desc = clean_html_description(raw_desc, feed_title)
            html_desc = generate_pivot_living_html(
                title=title,
                sku=sku if sku else item_id,
                hero_img=hero_img,
                gallery_imgs=gallery_imgs,
                clean_desc=clean_desc
            )

            writer.writerow(['Revise', item_id, html_desc])

    print(f"\n[DONE] Successfully wrote {len(items_to_revise)} rows to {output_file}.")
    print(f"Matched with supplier data: {matched_count}")
    print(f"Clean generic descriptions: {fallback_count}")

if __name__ == '__main__':
    main()
