# 🔄 Dropshipzone → eBay AU Bulk Listing Pipeline
### Complete Setup Guide — n8n + Cloudinary (No-Code)

---

## 📁 Files in This Folder

| File | Purpose |
|---|---|
| `n8n_workflow.json` | Import this into n8n — the complete workflow |
| `sample_dropshipzone_input.csv` | Example input format (Dropshipzone CSV) |
| `ebay_output_template.csv` | Example of the eBay CSV output this pipeline produces |
| `SETUP_GUIDE.md` | This file |

---

## 🏗️ Pipeline Overview

```
[Dropshipzone CSV]
        ↓
  [Parse CSV Rows]
        ↓
  [0] Pricing & Config  ← ✏️ Edit your rules here ONLY
        ↓
  [1] Title Transformer  (80-char limit + long-tail keywords)
        ↓
  [2] Price Calculator   (markup + eBay fee buffer + charm pricing)
        ↓
  [3] Filter Invalid Rows (skips zero-cost / no-image rows)
        ↓
  [4] Image Watermarker  (Cloudinary URL: Free Shipping + AU Stock + Ships in 24h)
        ↓
  [5] HTML Description Builder (full responsive HTML)
        ↓
  [6] eBay Row Assembler (maps to all eBay Seller Hub columns)
        ↓
  [7] Export eBay CSV
        ↓
  [8] Save to Disk → upload to eBay Seller Hub
```

---

## ⚙️ Step 1 — Set Up Cloudinary (Free)

Cloudinary is used to add watermark badges to your images **without downloading or editing any images manually**. It works 100% via URL.

1. Go to **https://cloudinary.com** → Sign up free
2. After signing in, go to **Dashboard**
3. Copy your **Cloud Name** (shown at the top, e.g. `my-store-au`)
4. In `n8n_workflow.json`, find this line inside **Node 0 · Pricing & Config**:
   ```
   cloudinaryCloudName: 'YOUR_CLOUD_NAME',
   ```
5. Replace `YOUR_CLOUD_NAME` with your actual cloud name

> **That's it for Cloudinary.** No uploads, no API keys needed for the fetch/transform approach.

### What the watermarks look like on the image:

```
┌─────────────────────────────────────────┐
│                                         │
│           [Product Image]               │
│                                         │
│ [FREE SHIPPING] [AU STOCK] [SHIPS 24H]  │
│  (green)         (blue)     (orange)    │
└─────────────────────────────────────────┘
```

### Customising badge colours (inside Node 0):
```js
badges: [
  { text: 'FREE%20SHIPPING', gravity: 'south_west', bg: 'green' },   // bottom-left
  { text: 'AU%20STOCK',      gravity: 'south',      bg: '0070c0' },  // bottom-centre
  { text: 'SHIPS%20IN%2024H',gravity: 'south_east', bg: 'e65c00' }   // bottom-right
]
```
Change `bg` to any hex colour or colour name.

---

## ⚙️ Step 2 — Set Up n8n

### Option A: n8n Cloud (Easiest, no server needed)
1. Go to **https://n8n.io** → Start free trial
2. Create a new workflow
3. Click the **...** menu → **Import from File**
4. Upload `n8n_workflow.json`

### Option B: n8n Desktop / Self-hosted
1. Install n8n: `npm install n8n -g`
2. Run: `n8n`
3. Open `http://localhost:5678`
4. Import `n8n_workflow.json`

---

## ⚙️ Step 3 — Configure Your Pricing (Node 0 Only)

**Open Node "0 · Pricing & Config"** and edit the CONFIG block at the top.
You only ever need to touch this one node to change pricing.

```js
const CONFIG = {
  // PRICING MODE — choose one:
  // 'percentage'  → price = cost × markupMultiplier
  // 'flat'        → price = cost + flatFee
  // 'combined'    → price = (cost × markupMultiplier) + flatFee  ← RECOMMENDED
  pricingMode: 'combined',
  markupMultiplier: 1.35,   // 35% markup over cost
  flatFee: 5.00,            // Extra $5 buffer on every item

  // eBay fee buffer (eBay AU = ~13.5%)
  ebayFeeRate: 0.135,
  applyEbayFeeBuffer: true, // true = price gross-up so you net your target after fees

  // Free shipping
  includeFreeShipping: true,       // Bake $X into price so listing shows FREE SHIPPING
  estimatedShippingCost: 8.50,    // Your actual avg shipping cost

  // Price floor — never sell below this
  minimumListingPrice: 9.99,

  // Charm pricing — e.g. $50.00 becomes $49.99
  charmPrice: true,
};
```

### Pricing Formula Example
If a product costs **$35.00**:
```
Step 1: $35.00 × 1.35 = $47.25
Step 2: $47.25 + $5.00 (flat fee) = $52.25
Step 3: $52.25 + $8.50 (shipping baked in) = $60.75
Step 4: $60.75 ÷ (1 - 0.135) = $70.23 (eBay fee gross-up)
Step 5: Floor check → $70.23 > $9.99 ✅
Step 6: Charm pricing → $69.99
Final listing price: $69.99
```

---

## ⚙️ Step 4 — Configure eBay Category IDs (Node 6)

In **Node "6 · eBay Row Assembler"**, there is a `CATEGORY_MAP` table.
Update it with your actual eBay category IDs.

To find an eBay AU category ID:
1. Go to **ebay.com.au** → Browse any category
2. The URL contains the category ID, e.g.:
   `https://www.ebay.com.au/b/Kitchen-Tools-Gadgets/20625/...`
   → Category ID = `20625`

---

## 🚀 Step 5 — Run the Pipeline

1. In n8n, open the imported workflow
2. Click the **"📂 Trigger: Read CSV File"** node
3. Set the **File Path** to your Dropshipzone CSV file location
4. Click **"Execute Workflow"**
5. The output CSV will be saved to the same folder as your input file
   - Filename: `YYYYMMDD_HHMM_ebay_upload.csv`

---

## 📤 Step 6 — Upload to eBay

1. Go to **eBay Seller Hub** → **Listings** → **Create Listings** → **File upload**
2. Upload the generated `_ebay_upload.csv`
3. Review the upload summary — fix any errors
4. Activate listings

---

## 🗺️ Dropshipzone CSV Column Mapping

The pipeline automatically detects these column names from Dropshipzone exports:

| Dropshipzone Column | Used For |
|---|---|
| `Product Name` / `Title` / `Name` | eBay title (transformed) |
| `SKU` / `Product Code` | Custom Label, internal tracking |
| `DSZ Price` / `Cost Price` / `Price` | Price calculation base |
| `Image URL` / `Image URLs` / `Images` | Watermarked PicURL |
| `Description` / `Short Description` | HTML description body |
| `Brand` / `Manufacturer` | Item specific + description |
| `Category` / `Sub Category` | eBay category lookup |
| `Stock` / `Stock Level` / `Quantity` | Listing quantity |
| `Weight (kg)` / `Weight` | Shipping weight |
| `Colour` / `Color` | Item specific |
| `Material` | Item specific |
| `Model` / `Model Number` | Item specific |
| `Dimensions` / `Size` | Item specific |
| `Warranty` | Description trust badge |

> If your Dropshipzone export uses different column names, update the column name strings in Nodes 1–6.

---

## 🛡️ Validation & Error Handling

The pipeline includes built-in safety guards:

| Check | What Happens |
|---|---|
| Cost = 0 or missing | Row is **flagged and filtered out** — not uploaded |
| No image URL | Row is flagged with `_image_error` warning |
| Title > 80 chars | Automatically truncated at word boundary |
| Price below floor | Bumped up to `minimumListingPrice` |
| Quantity = 0 | Defaults to 1 (prevents zero-stock listings) |

---

## 📊 Output Columns Produced

Every row in the output CSV contains:

**eBay required fields:**
`*Action`, `*Title`, `*Category`, `CustomLabel`, `*ConditionID`, `*StartPrice`, `*Quantity`, `*Format`, `*Duration`, `ShippingType`, `Country`, `*Location`, `PicURL`, `Description`

**eBay shipping fields:**
`ShippingService-1:Option`, `ShippingService-1:Cost`, `DispatchTimeMax`, `ShipToLocations`

**eBay returns fields:**
`ReturnsAcceptedOption`, `ReturnsWithin`, `RefundOption`, `ShippingCostPaidBy`

**eBay item specifics:**
`C:Brand`, `C:Type`, `C:Model`, `C:Colour`, `C:Material`, `C:Size`

**Internal tracking (not uploaded to eBay):**
`_supplier_sku`, `_cost`, `_profit_estimate`

---

## 💡 Tips

- **Test with 3–5 rows first** before running your full Dropshipzone catalog
- **Check Cloudinary image rendering** — paste a generated URL into your browser to verify watermarks look correct
- **eBay category IDs** are the most important field to get right — wrong category = poor search visibility
- **Title keywords** — edit the `KEYWORD_MAP` in Node 1 to add category-specific long-tail keywords relevant to your products
- **Profit tracking** — the `_profit_estimate` column lets you review margin before uploading

---

## 🆘 Common Issues

| Problem | Fix |
|---|---|
| Cloudinary image returns 404 | Make sure your Cloud Name is correct in Node 0 |
| All prices are wrong | Check that your CSV uses `DSZ Price` or `Cost Price` column name |
| eBay rejects the CSV | Download the template from eBay Seller Hub first to verify expected column names |
| Titles are too long | The pipeline already caps at 80 chars — check `_ebay_title` in output |
| Description shows raw HTML | This is correct — eBay renders HTML in the Description column |
