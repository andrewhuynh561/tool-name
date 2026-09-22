# Store Context & Auto-Detection Rules for eBay Australia Stores

This rule governs how agents and execution pipelines differentiate and handle requests across the two distinct eBay Australia stores in this workspace.

---

## 1. Quick Detection Matrix

When the user drops a store file, specifies a store name, mentions a title keyword, or drops a CSV feed with store context, immediately map to the correct store configuration:

| Detection Trigger / Clues | Store Selected | Store Name | Title Suffix | SKU Prefix | Delta Snapshot File | Output CSV |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `store1.txt`, `store1`, `pivot`, `pivotliving`, `AU Stock` | **Store 1** | `PivotLiving` | ` AU Stock` | `DSZ-` | `pipeline/snapshots/seen_skus.txt` | `output_ebay_upload_store1.csv` |
| `store2.txt`, `store2`, `agv`, `augoodvantage`, `AU Fast Post`, `AU Postage` | **Store 2** | `AuGoodVantage` | ` AU Fast Post` | `AGV-` | `pipeline/snapshots/store2_seen_skus.txt` | `output_ebay_upload_store2.csv` |

---

## 2. Store Profiles & Parameters

### Store 1: PivotLiving (`PivotLiving`)
* **Config File**: `watermark/store1.txt`
* **Store URL**: [https://www.ebay.com.au/str/pivotliving](https://www.ebay.com.au/str/pivotliving)
* **Custom SKU Format**: `DSZ-{SUPPLIER_SKU}` (e.g. `DSZ-V1263-JX-3024`)
* **eBay Cassini Title**: Ends strictly with **` AU Stock`** (80-character maximum, natural word boundary truncation).
* **Hero Watermark**: Cloudinary Public ID `ChatGPT_Image_Aug_26_2026_12_31_37_AM` (South gravity, 100% width, 95% opacity).
* **HTML Listing Template**: `pivot_living_template_preview.html` (Artisanal warm neutral theme `#F7F5F0` / `#2C3135`).
* **Delta Snapshot File**: `pipeline/snapshots/seen_skus.txt` (Also references `active_skus_20260903.txt` & `active_listings.csv`).
* **Pricing Formula**: `RRP + $5.00` flat fee with `.99` charm price (`charmPrice: True`, e.g. `$39.99`).
* **Output Destinations**:
  * Workspace: `pipeline/output_ebay_upload_store1.csv`
  * Root: `output_ebay_upload_store1.csv`
  * Downloads New Batch: `C:/Users/andre/Downloads/output_ebay_upload_store1_{feed_key}_new_batch.csv`
  * Downloads Full Catalog: `C:/Users/andre/Downloads/output_ebay_upload_store1_all.csv`
* **Pipeline Run Command**:
  ```bash
  python pipeline/run_n8n_pipeline.py <path_to_feed_csv> --store store1 --delta
  ```

---

### Store 2: AuGoodVantage (`AuGoodVantage`)
* **Config File**: `watermark/store2.txt`
* **Store URL**: [https://www.ebay.com.au/str/augoodvantage](https://www.ebay.com.au/str/augoodvantage)
* **Custom SKU Format**: `AGV-{SUPPLIER_SKU}` (e.g. `AGV-V1263-JX-3024`)
* **eBay Cassini Title**: Ends strictly with **` AU Fast Post`** (aliases: `AU Postage`, `AU Fast Postage`).
* **Supplier Brand Stripping**: Strips supplier brands from the title start: `Landhoow`, `Weisshorn`, `Everfit`, `Alritz`, `JIALWEN`, `TAMOSH`.
* **Hero Watermark**: Cloudinary Public ID `OpenAI_Playground_2026-09-05_at_21.54.57` (South gravity, 100% width, 95% opacity).
* **HTML Listing Template**: `augoodvantage_template_preview.html` (Modern coral / slate theme `#FFFFFF` / `#FCF8F7` / `#E5A19C` / `#4E5361`).
* **Delta Snapshot File**: `pipeline/snapshots/store2_seen_skus.txt`.
* **Pricing Formula**: `RRP + $5.00` flat fee without charm pricing (`charmPrice: False`, exact rounded cents e.g. `$45.50`).
* **Output Destinations**:
  * Workspace: `pipeline/output_ebay_upload_store2.csv`
  * Root: `output_ebay_upload_store2.csv`
  * Downloads New Batch: `C:/Users/andre/Downloads/output_ebay_upload_store2_{feed_key}_new_batch.csv`
  * Downloads Full Catalog: `C:/Users/andre/Downloads/output_ebay_upload_store2_all.csv`
* **Pipeline Run Command**:
  ```bash
  python pipeline/run_n8n_pipeline.py <path_to_feed_csv> --store store2 --delta
  ```

---

## 3. Operational Rules for New CSV Feeds

1. **Always Use Delta Mode (`--delta`)**:
   Never re-list items that already exist in that store's snapshot. The pipeline reads the respective `seen_skus.txt` or `store2_seen_skus.txt` to guarantee zero duplicate listings and protect monthly selling limits.
2. **Automatic Store Fallback**:
   If the user does not specify a store flag but mentions `store1` / `store2` or drops the config file `store1.txt` / `store2.txt`, the agent and pipeline will automatically resolve the store without asking redundant questions.
