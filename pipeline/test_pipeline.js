const fs = require('fs');
const path = require('path');

// 1. Read input CSV
const csvPath = '/data/ebay/sample_dropshipzone_input.csv';
const csvContent = fs.readFileSync(csvPath, 'utf8');

// Parse TSV/CSV manually (Dropshipzone tab-separated or comma-separated)
const lines = csvContent.split('\n').filter(l => l.trim().length > 0);
const delimiter = csvContent.includes('\t') ? '\t' : ',';

function parseCSVLine(text) {
  const result = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (inQuotes && text[i+1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === delimiter && !inQuotes) {
      result.push(cur.trim());
      cur = '';
    } else {
      cur += c;
    }
  }
  result.push(cur.trim());
  return result;
}

const headers = parseCSVLine(lines[0]);
console.log('Detected Headers count:', headers.length);
console.log('Headers:', headers.slice(0, 10));

const items = [];
// For multi-line TSV fields (like Description with newlines inside quotes), let's parse using proper CSV/TSV regex
let fullText = lines.slice(1).join('\n');
// Match TSV rows properly
const rows = [];
let curRow = [];
let curCell = '';
let insideQuotes = false;
for (let i = 0; i < csvContent.length; i++) {
  const char = csvContent[i];
  if (char === '"') {
    if (insideQuotes && csvContent[i+1] === '"') {
      curCell += '"';
      i++;
    } else {
      insideQuotes = !insideQuotes;
    }
  } else if (char === '\t' && !insideQuotes) {
    curRow.push(curCell.trim());
    curCell = '';
  } else if ((char === '\n' || char === '\r') && !insideQuotes) {
    if (char === '\r' && csvContent[i+1] === '\n') i++;
    curRow.push(curCell.trim());
    if (curRow.length >= headers.length) {
      rows.push(curRow);
    }
    curRow = [];
    curCell = '';
  } else {
    curCell += char;
  }
}

const parsedItems = rows.map(r => {
  const obj = {};
  headers.forEach((h, idx) => { obj[h] = r[idx] || ''; });
  return obj;
});

console.log(`Parsed ${parsedItems.length} complete items.`);
if (parsedItems.length > 0) {
  console.log('Sample Item Image 1:', parsedItems[0]['Image 1']);
}

// 2. Execute Node 0 (Config)
const CONFIG = {
  cloudinaryCloudName: 'smqochzy',
  watermarkPublicId: 'rm_deliverandfree',
  watermarkGravity: 'north_west',
  watermarkWidthPct: 100,
  watermarkXOffset: 0,
  watermarkYOffset: -20,
  watermarkOpacity: 95,
  pricingMode: 'combined',
  markupMultiplier: 1.35,
  flatFee: 5.00,
  ebayFeeRate: 0.135,
  applyEbayFeeBuffer: true,
  includeFreeShipping: true,
  useFixedShipping: false,
  estimatedShippingCost: 9.90,
  shippingFallback: 9.90,
  applyActiveRebate: true,
  minimumListingPrice: 9.99,
  charmPrice: true
};

const CATEGORY_MAP = {
  'Pickleball': '43311',
  'Pet': '1281',
  'Massage': '36444',
  'Yoga': '158086',
  'Sports': '382',
  'Tools': '631',
  'default': '11700'
};

function toBase64(str) {
  return Buffer.from(str).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

// 3. Process every row through all nodes
const ebayRows = [];

parsedItems.forEach((item, index) => {
  console.log(`--- Processing Product #${index + 1}: ${item.SKU} ---`);

  // Node 1: Title Cleaner
  const rawTitle = (item['Title'] || '').trim();
  let cleanedTitle = rawTitle
    .replace(/^[A-Z0-9]{2,}-[A-Z0-9-]+\s+/i, '')
    .replace(/^(Black|White|Grey|Gray|Red|Blue|Green|Yellow|Pink|Purple|Orange|Brown|Silver|Gold|Beige|Khaki|Navy|Cream|Clear|Dark|Light)\s+/i, '')
    .replace(/\s{2,}/g, ' ')
    .trim();

  // Trim to 80 chars max & append AU Stock
  let finalTitle = cleanedTitle;
  if ((finalTitle + ' AU Stock').length <= 80) {
    finalTitle += ' AU Stock';
  } else {
    finalTitle = finalTitle.substring(0, 80).trim();
  }
  console.log(`  [Title]: ${finalTitle} (${finalTitle.length} chars)`);

  // Node 4: Price Calculator
  const costRaw = item['Cost per item'] || item['Price'] || '0';
  let cost = parseFloat(String(costRaw).replace(/[^0-9.]/g, '')) || 0;
  
  // Rebate check
  let rebateApplied = 0;
  const rebatePct = parseFloat(item['Rebate %'] || '0') || 0;
  if (rebatePct > 0) {
    rebateApplied = cost * (rebatePct / 100);
    cost -= rebateApplied;
  }

  // Metro shipping lookup
  const metroCols = ['Delivery(ACT)', 'Delivery(NSW_M)', 'Delivery(QLD_M)', 'Delivery(SA_M)', 'Delivery(VIC_M)', 'Delivery(WA_M)'];
  const metroVals = metroCols.map(c => parseFloat(String(item[c] || '0').replace(/[^0-9.]/g, ''))).filter(v => v > 0);
  const shippingCost = metroVals.length > 0 ? Math.max(...metroVals) : CONFIG.shippingFallback;

  // Calculation
  let price = (cost * CONFIG.markupMultiplier) + CONFIG.flatFee;
  if (CONFIG.includeFreeShipping) price += shippingCost;
  if (CONFIG.applyEbayFeeBuffer) price = price / (1 - CONFIG.ebayFeeRate);
  if (price < CONFIG.minimumListingPrice) price = CONFIG.minimumListingPrice;
  if (CONFIG.charmPrice && price > 1) price = Math.ceil(price) - 0.01;

  const finalPriceStr = price.toFixed(2);
  const ebayFee = (price * CONFIG.ebayFeeRate).toFixed(2);
  const profitEst = (price - cost - shippingCost - parseFloat(ebayFee)).toFixed(2);
  const marginPct = ((parseFloat(profitEst) / price) * 100).toFixed(1);

  console.log(`  [Pricing]: Cost: $${cost.toFixed(2)} | Shipping: $${shippingCost.toFixed(2)} | Sell Price: $${finalPriceStr} | Profit: $${profitEst} (${marginPct}%)`);

  // Node 6: Image Watermarker
  const imageList = [item['Image 1'], item['Image 2'], item['Image 3'], item['Image 4'], item['Image 5'], item['Image 6']]
    .map(u => (u || '').trim()).filter(u => u.length > 0 && u.startsWith('http'));

  const primaryUrl = imageList[0] || '';
  const widthScale = (CONFIG.watermarkWidthPct / 100).toFixed(2);
  const watermarkLayer = `l_${CONFIG.watermarkPublicId},w_1.0,c_scale,g_north,y_0,fl_relative`;
  const watermarkedPrimary = `https://res.cloudinary.com/${CONFIG.cloudinaryCloudName}/image/fetch/${watermarkLayer}/${primaryUrl}`;
  
  const allImages = [watermarkedPrimary, ...imageList.slice(1)];
  const picURLs = allImages.join('|');
  console.log(`  [Watermarked Primary Image URL]: ${watermarkedPrimary}`);

  // Node 7: HTML Description Builder
  const rawDesc = item['Description'] || '';
  const cleanText = rawDesc.replace(/<img[^>]+>/gi, '').replace(/<[^>]+>/g, ' ').replace(/\s{2,}/g, ' ').trim();
  const htmlDesc = `<div style="max-width:800px;font-family:Arial"><h1 style="font-size:18px">${finalTitle}</h1><div style="background:#f4f6f9;padding:12px"><h3>Key Features</h3><p>${cleanText.substring(0, 300)}...</p></div></div>`;

  // Category matching
  const cat = item['Category'] || '';
  const subcat = item['Subcategory'] || '';
  const subsubcat = item['Sub_subcategory'] || '';
  let categoryId = CATEGORY_MAP['default'];
  for (const level of [subsubcat, subcat, cat]) {
    if (!level) continue;
    for (const [k, v] of Object.entries(CATEGORY_MAP)) {
      if (level.toLowerCase().includes(k.toLowerCase())) { categoryId = v; break; }
    }
    if (categoryId !== CATEGORY_MAP['default']) break;
  }

  // Node 8: eBay Row
  const qty = parseInt(item['QOH'] || '0', 10);
  const ebayRow = {
    '*Action': 'Add',
    '*Title': finalTitle,
    '*Category': categoryId,
    'CustomLabel': `DSZ-${item.SKU}`,
    '*ConditionID': '1000',
    '*StartPrice': finalPriceStr,
    '*Quantity': qty > 0 ? qty : 1,
    '*Format': 'FixedPrice',
    '*Duration': 'GTC',
    'ShippingType': 'Free',
    'ShippingService-1:Option': 'AU_StandardDelivery',
    'ShippingService-1:Cost': '0.00',
    'DispatchTimeMax': '1',
    'Country': 'AU',
    '*Location': 'Australia',
    'PicURL': picURLs,
    'Description': htmlDesc,
    '_dsz_sku': item.SKU,
    '_cost': cost.toFixed(2),
    '_shipping': shippingCost.toFixed(2),
    '_profit': profitEst,
    '_margin': marginPct + '%'
  };

  ebayRows.push(ebayRow);
});

// 4. Output CSV Generation
function toCSV(rows) {
  if (rows.length === 0) return '';
  const cols = Object.keys(rows[0]);
  const headerLine = cols.map(c => `"${c.replace(/"/g, '""')}"`).join(',');
  const bodyLines = rows.map(r => cols.map(c => `"${String(r[c] || '').replace(/"/g, '""')}"`).join(','));
  return [headerLine, ...bodyLines].join('\n');
}

const outputCSV = toCSV(ebayRows);
const outputPath = '/data/ebay/pipeline/output_ebay_upload.csv';
fs.writeFileSync(outputPath, outputCSV, 'utf8');

console.log(`\n=======================================================`);
console.log(`✅ Pipeline Test Executed Successfully!`);
console.log(`Output CSV generated: ${outputPath}`);
console.log(`Processed ${ebayRows.length} items with complete pricing, titles, and watermarks.`);
console.log(`=======================================================\n`);
