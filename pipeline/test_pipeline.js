const fs = require('fs');
const path = require('path');

// 1. Read input CSV (support both local Windows and Docker environments)
let csvPath = path.join(__dirname, '..', 'sample_dropshipzone_input.csv');
if (!fs.existsSync(csvPath)) {
  csvPath = '/data/ebay/sample_dropshipzone_input.csv';
}
if (!fs.existsSync(csvPath)) {
  csvPath = path.join(__dirname, 'sample_dropshipzone_input.csv');
}

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
  } else if (char === delimiter && !insideQuotes) {
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

// Skip header row if included
const dataRows = (rows.length > 0 && rows[0][0] === headers[0]) ? rows.slice(1) : rows;

const parsedItems = dataRows.map(r => {
  const obj = {};
  headers.forEach((h, idx) => { obj[h] = r[idx] || ''; });
  return obj;
});

console.log(`Parsed ${parsedItems.length} complete items from feed.`);

// 2. Master Config
const CONFIG = {
  cloudinaryCloudName: 'smqochzy',
  watermarkPublicId: 'ChatGPT_Image_Aug_26_2026_12_31_37_AM',
  watermarkGravity: 'south',
  watermarkWidthPct: 100,
  watermarkXOffset: 0,
  watermarkYOffset: 0,
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
  charmPrice: true,
  maxListingQuantity: 3 // Cap quantity to protect eBay seller allowance and avoid limit errors
};

// Official eBay Australia (Site ID 15) Leaf Category Taxonomy
const CATEGORY_MAP = {
  'pickleball': '184357',     // Sporting Goods > Racquet Sports > Pickleball > Paddles (LIVE)
  'grooming': '177794',       // Pet Supplies > Dog Supplies > Grooming > Clippers & Blades (LIVE)
  'clipper': '177794',        // Pet Supplies > Dog Supplies > Grooming > Clippers & Blades (LIVE)
  'pet cleaning': '177794',   // Pet Supplies > Dog Supplies > Grooming > Clippers & Blades (LIVE)
  'massage gun': '36449',     // Health & Beauty > Massage > Massagers
  'massager': '36449',        // Health & Beauty > Massage > Massagers
  'massage': '36449',         // Health & Beauty > Massage > Massagers
  'yoga mat': '158929',       // Sporting Goods > Fitness > Yoga & Pilates > Mat Carriers & Bags
  'yoga': '158929',           // Sporting Goods > Fitness > Yoga & Pilates > Mat Carriers & Bags
  'pilates': '158929',        // Sporting Goods > Fitness > Yoga & Pilates > Mat Carriers & Bags
  'laptop stand': '175685',   // Computers/Tablets & Networking > Laptop Accessories > Laptop Stands & Risers
  'chopper': '20638',         // Home & Garden > Kitchen Tools & Gadgets > Choppers & Mincers
  'kitchen': '20638',
  'fan': '43509',             // Home Appliances > Heating, Cooling & Air > Portable Fans
  'headlamp': '106988',       // Sporting Goods > Camping & Hiking > Flashlights & Headlamps
  'kegel': '15280',           // Sporting Goods > Fitness, Running & Yoga > Strength Training
  'thigh': '15280',
  'radio': '96954',           // Sound & Vision > Portable Audio > Portable AM/FM Radios
  'cat carrier': '177789',    // Pet Supplies > Cat Supplies > Beds
  'cat shelter': '177789',
  'christmas': '170090',      // Home & Garden > Holiday & Seasonal Decor > Ornaments
  'pillow': '20563',          // Home & Garden > Bedding > Pillows
  'wallet': '2996',           // Clothing, Shoes & Accessories > Men's Accessories > Wallets
  'cat toy': '20741',         // Pet Supplies > Cat Supplies > Cat Toys
  'sewing': '20160',          // Crafts > Sewing > Sewing Machines
  'table lamp': '20702',      // Home & Garden > Lamps, Lighting & Ceiling Fans > Lamps
  'bottle lamp': '20702',
  'shower': '181379',         // Sporting Goods > Camping & Hiking > Camp Sanitation
  'hiking pole': '84886',     // Sporting Goods > Camping & Hiking > Hiking Poles
  'trekking': '84886',
  'mouse': '23160',           // Computers/Tablets & Networking > Keyboards, Mice & Pointers > Mice
  'chest rig': '177880',      // Sporting Goods > Hunting > Tactical Bags & Packs
  'water bag': '181381',      // Sporting Goods > Camping & Hiking > Water Storage
  'ankle brace': '36449',     // Health & Beauty > Massage > Massagers
  'battle rope': '179803',    // Sporting Goods > Fitness, Running & Yoga > Exercise Straps & Ropes
  'flosser': '106095',        // Health & Beauty > Oral Care > Dental Floss & Flossers
  'oral care': '106095',
  'watch': '178893',          // Smart Watches & Fitness Trackers
  'wristband': '178893',
  'scrubber': '20636',        // Home & Garden > Household Cleaning Products > Cleaning Brushes
  'lunch bag': '54316',       // Home & Garden > Kitchen, Dining & Bar > Food Storage > Lunch Bags
  'hair dryer': '101419',     // Health & Beauty > Hair Care & Styling > Hair Dryers
  'lock picking': '183831',   // Business & Industrial > Access Control > Locksmith Equipment > Locksmithing Tools
  'gravity pick': '183831',
  'tools': '183831',
  'backpack': '169291',       // Clothing, Shoes & Accessories > Women's Bags & Handbags
  'hobo bag': '169291',
  'handbag': '169291',
  'default': '11700'
};

// Item Specifics Extractor
function extractSpecs(item, cleanTitle) {
  const desc = item['Description'] || '';
  const title = item['Title'] || '';
  const text = `${title} ${desc}`.toLowerCase();

  // 1. Material
  let material = 'High Quality Material';
  const matMatches = [
    { key: 'carbon fiber', val: 'Carbon Fiber' },
    { key: 'fiberglass', val: 'Fiberglass' },
    { key: 'stainless steel', val: 'Stainless Steel' },
    { key: 'aluminum alloy', val: 'Aluminum Alloy' },
    { key: 'aluminium', val: 'Aluminium Alloy' },
    { key: 'pu leather', val: 'PU Leather' },
    { key: 'memory foam', val: 'Memory Foam' },
    { key: 'oxford cloth', val: 'Oxford Fabric' },
    { key: 'oxford fabric', val: 'Oxford Fabric' },
    { key: 'canvas', val: 'Canvas' },
    { key: 'corduroy', val: 'Corduroy' },
    { key: 'abs plastic', val: 'ABS Plastic' },
    { key: 'abs', val: 'ABS Plastic' },
    { key: 'silicone', val: 'Silicone' },
    { key: 'tpe', val: 'TPE' },
    { key: 'pvc', val: 'Heavy Duty PVC' }
  ];
  for (const m of matMatches) {
    if (text.includes(m.key)) { material = m.val; break; }
  }

  // 2. Colour
  let colour = 'Multicoloured';
  const colours = ['Black', 'White', 'Grey', 'Gray', 'Blue', 'Pink', 'Purple', 'Green', 'Silver', 'Gold', 'Yellow', 'Khaki', 'Beige', 'Red', 'Orange'];
  for (const c of colours) {
    if (new RegExp(`\\b${c}\\b`, 'i').test(title) || new RegExp(`color[s]?:?\\s*${c}`, 'i').test(desc)) {
      colour = c === 'Gray' ? 'Grey' : c;
      break;
    }
  }

  // 3. Power Source
  let power = 'Manual / Non-Electric';
  if (text.includes('solar')) power = 'Solar Powered';
  else if (text.includes('usb rechargeable') || text.includes('rechargeable')) power = 'USB Rechargeable Battery';
  else if (text.includes('usb powered') || text.includes('usb')) power = 'USB Powered';
  else if (text.includes('battery')) power = 'Battery Powered';

  // 4. Type
  let type = item['Sub_subcategory'] || item['Subcategory'] || item['Category'] || 'General Merchandise';
  if (type === 'default' || type === '0') type = 'Accessories';

  // 5. Features
  const featuresList = [];
  if (text.includes('portable')) featuresList.push('Portable');
  if (text.includes('lightweight')) featuresList.push('Lightweight');
  if (text.includes('rechargeable')) featuresList.push('Rechargeable');
  if (text.includes('waterproof') || text.includes('water resistance')) featuresList.push('Waterproof');
  if (text.includes('ergonomic')) featuresList.push('Ergonomic');
  if (text.includes('adjustable')) featuresList.push('Adjustable');
  if (text.includes('foldable') || text.includes('collapsible')) featuresList.push('Foldable');
  if (text.includes('quiet') || text.includes('low noise')) featuresList.push('Ultra Quiet');
  const features = featuresList.slice(0, 5).join(', ') || 'Durable, Easy to Use';

  // 6. Department (Mandatory for Handbags, Apparel, Accessories)
  let department = 'Unisex Adults';
  if (/\b(women|woman|ladies|lady|girls)\b/i.test(text) || text.includes('hobo bag') || text.includes('handbag')) department = 'Women';
  else if (/\b(men|man|gentlemen|boys)\b/i.test(text) && !/\b(women|woman|ladies)\b/i.test(text)) department = 'Men';

  // 7. Style (Mandatory for Handbags, Bags)
  let style = 'Modern';
  if (text.includes('hobo')) style = 'Hobo Bag';
  else if (text.includes('tote')) style = 'Tote';
  else if (text.includes('shoulder bag') || text.includes('shoulder purse')) style = 'Shoulder Bag';
  else if (/\bbackpack\b/i.test(text)) style = 'Backpack';
  else if (text.includes('chest rig')) style = 'Tactical Bag';
  else if (text.includes('crossbody')) style = 'Crossbody';

  return {
    brand: 'Unbranded',
    type: type,
    material: material,
    colour: colour,
    power: power,
    features: features,
    department: department,
    style: style,
    mpn: `DSZ-${item.SKU}`
  };
}

// 3. Process every row through all nodes
const ebayRows = [];

parsedItems.forEach((item, index) => {
  if (!item.SKU || !item.Title) return;

  // Node 1: Title Cleaner (Strip supplier code, model prefix, color prefix)
  const rawTitle = (item['Title'] || '').trim();
  let cleanedTitle = rawTitle
    .replace(/^[A-Z0-9]{2,}-[A-Z0-9-]+\s+/i, '')
    .replace(/^LC-[A-Z0-9-]+\s+/i, '')
    .replace(/^(Black|White|Grey|Gray|Red|Blue|Green|Yellow|Pink|Purple|Orange|Brown|Silver|Gold|Beige|Khaki|Navy|Cream|Clear|Dark|Light)\s+/i, '')
    .replace(/\s{2,}/g, ' ')
    .trim();

  // Cassini Title Formatting (Target 75-80 chars, word-boundary safe, append AU Stock)
  let finalTitle = cleanedTitle;
  if (!finalTitle.toLowerCase().includes('au stock')) {
    if ((finalTitle + ' AU Stock').length <= 80) {
      finalTitle += ' AU Stock';
    } else {
      const maxLen = 80 - ' AU Stock'.length;
      let truncated = finalTitle.substring(0, maxLen);
      const lastSpace = truncated.lastIndexOf(' ');
      if (lastSpace > 35) truncated = truncated.substring(0, lastSpace);
      finalTitle = `${truncated} AU Stock`;
    }
  } else if (finalTitle.length > 80) {
    let truncated = finalTitle.substring(0, 80);
    const lastSpace = truncated.lastIndexOf(' ');
    finalTitle = lastSpace > 45 ? truncated.substring(0, lastSpace) : truncated;
  }

  // Node 4: Price Calculator
  const costRaw = item['Cost per item'] || item['Price'] || '0';
  let cost = parseFloat(String(costRaw).replace(/[^0-9.]/g, '')) || 0;
  
  let rebateApplied = 0;
  const rebatePct = parseFloat(item['Rebate %'] || '0') || 0;
  if (rebatePct > 0) {
    rebateApplied = cost * (rebatePct / 100);
    cost -= rebateApplied;
  }

  const metroCols = ['Delivery(ACT)', 'Delivery(NSW_M)', 'Delivery(QLD_M)', 'Delivery(SA_M)', 'Delivery(VIC_M)', 'Delivery(WA_M)'];
  const metroVals = metroCols.map(c => parseFloat(String(item[c] || '0').replace(/[^0-9.]/g, ''))).filter(v => v > 0);
  const shippingCost = metroVals.length > 0 ? Math.max(...metroVals) : CONFIG.shippingFallback;

  let price = (cost * CONFIG.markupMultiplier) + CONFIG.flatFee;
  if (CONFIG.includeFreeShipping) price += shippingCost;
  if (CONFIG.applyEbayFeeBuffer) price = price / (1 - CONFIG.ebayFeeRate);
  if (price < CONFIG.minimumListingPrice) price = CONFIG.minimumListingPrice;
  if (CONFIG.charmPrice && price > 1) price = Math.ceil(price) - 0.01;

  const finalPriceStr = price.toFixed(2);
  const ebayFee = (price * CONFIG.ebayFeeRate).toFixed(2);
  const profitEst = (price - cost - shippingCost - parseFloat(ebayFee)).toFixed(2);
  const marginPct = ((parseFloat(profitEst) / price) * 100).toFixed(1);

  // Node 6: Image Watermarker (Option A: Watermark ONLY Image 1 as Main Hero Image)
  const imageList = [item['Image 1'], item['Image 2'], item['Image 3'], item['Image 4'], item['Image 5'], item['Image 6']]
    .map(u => (u || '').trim()).filter(u => u.length > 0 && u.startsWith('http'));

  const widthScale = (CONFIG.watermarkWidthPct / 100).toFixed(2);
  const watermarkLayer = `l_${CONFIG.watermarkPublicId},w_${widthScale},c_scale,g_${CONFIG.watermarkGravity},x_${CONFIG.watermarkXOffset},y_${CONFIG.watermarkYOffset},o_${CONFIG.watermarkOpacity},fl_relative`;
  const allImages = imageList.map((url, idx) => idx === 0 ? `https://res.cloudinary.com/${CONFIG.cloudinaryCloudName}/image/fetch/${watermarkLayer}/${url}` : url);
  const picURLs = allImages.join('|');

  // Node 7: HTML Description Builder
  const rawDesc = item['Description'] || '';
  const cleanText = rawDesc.replace(/<img[^>]+>/gi, '').replace(/<[^>]+>/g, ' ').replace(/\s{2,}/g, ' ').trim();
  const htmlDesc = `<div style="max-width:800px;font-family:Arial,sans-serif;"><h1 style="font-size:18px;color:#111;">${finalTitle}</h1><div style="background:#f4f6f9;padding:14px;border-radius:6px;"><h3>Key Features</h3><p>${cleanText.substring(0, 350)}...</p></div></div>`;

  // Category matching
  const cat = item['Category'] || '';
  const subcat = item['Subcategory'] || '';
  const subsubcat = item['Sub_subcategory'] || '';
  const searchText = `${subsubcat} ${subcat} ${cat} ${finalTitle}`.toLowerCase();
  let categoryId = CATEGORY_MAP['default'];
  for (const [k, v] of Object.entries(CATEGORY_MAP)) {
    if (k !== 'default' && searchText.includes(k)) {
      categoryId = v;
      break;
    }
  }

  // Extract Item Specifics
  const specs = extractSpecs(item, finalTitle);

  // Node 8: eBay Bulk Upload Row with Cassini Item Specifics & Capped Quantity
  const rawQty = parseInt(item['QOH'] || '0', 10);
  const listQty = Math.min(rawQty > 0 ? rawQty : 1, CONFIG.maxListingQuantity);

  const ebayRow = {
    '*Action': 'Add',
    '*Title': finalTitle,
    '*Category': categoryId,
    'CustomLabel': `DSZ-${item.SKU}`,
    '*ConditionID': '1000',
    '*StartPrice': finalPriceStr,
    '*Quantity': listQty,
    '*Format': 'FixedPrice',
    '*Duration': 'GTC',
    'ShippingType': 'Free',
    'ShippingService-1:Option': 'AU_StandardDelivery',
    'ShippingService-1:Cost': '0.00',
    'DispatchTimeMax': '1',
    'Country': 'AU',
    '*Location': 'Australia',
    'PicURL': picURLs,
    'C:Brand': specs.brand,
    'C:Type': specs.type,
    'C:Material': specs.material,
    'C:Colour': specs.colour,
    'C:Department': specs.department,
    'C:Style': specs.style,
    'C:Power Source': specs.power,
    'C:Features': specs.features,
    'C:MPN': specs.mpn,
    'Description': htmlDesc,
    '_dsz_sku': item.SKU,
    '_cost': cost.toFixed(2),
    '_shipping': shippingCost.toFixed(2),
    '_profit': profitEst,
    '_margin': marginPct + '%'
  };

  ebayRows.push(ebayRow);
  console.log(`[#${index+1}] ${item.SKU} | Cat: ${categoryId} | Title: ${finalTitle} (${finalTitle.length}ch) | Sell: $${finalPriceStr} | Profit: $${profitEst} (${marginPct}%)`);
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
let outputPath = path.join(__dirname, 'output_ebay_upload.csv');
fs.writeFileSync(outputPath, outputCSV, 'utf8');

console.log(`\n=======================================================`);
console.log(`✅ Successfully Processed ${ebayRows.length} Winning Dropshipzone Products!`);
console.log(`📁 Exported to: ${outputPath}`);

console.log(`Output CSV generated: ${outputPath}`);
console.log(`Processed ${ebayRows.length} items with complete pricing, titles, and watermarks.`);
console.log(`=======================================================\n`);
