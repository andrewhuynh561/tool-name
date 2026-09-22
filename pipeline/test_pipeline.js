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
      if (inQuotes && text[i + 1] === '"') {
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
    if (insideQuotes && csvContent[i + 1] === '"') {
      curCell += '"';
      i++;
    } else {
      insideQuotes = !insideQuotes;
    }
  } else if (char === delimiter && !insideQuotes) {
    curRow.push(curCell.trim());
    curCell = '';
  } else if ((char === '\n' || char === '\r') && !insideQuotes) {
    if (char === '\r' && csvContent[i + 1] === '\n') i++;
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
  'pickleball': '184357',
  'grooming': '177794',
  'clipper': '177794',
  'pet': '177794',
  'cat': '177789',
  'dog': '177794',
  'bird': '177794',
  'massage': '36449',
  'massager': '36449',
  'yoga': '158929',
  'fitness': '179803',
  'gym': '179803',
  'exercise': '179803',
  'push up': '179803',
  'laptop': '175685',
  'computer': '175685',
  'chopper': '20638',
  'kitchen': '20638',
  'cookware': '20638',
  'press': '20638',
  'food storage': '20635',
  'container': '20635',
  'storage': '20635',
  'fan': '43509',
  'headlamp': '16037',
  'flashlight': '16037',
  'kegel': '15280',
  'pelvic': '15280',
  'radio': '96954',
  'speaker': '96954',
  'christmas': '170091',
  'halloween': '170091',
  'costume': '170091',
  'pillow': '20563',
  'cushion': '20563',
  'towel': '20572',
  'mat': '20572',
  'canopy': '20563',
  'diffuser': '20561',
  'aroma': '20561',
  'humidifier': '20561',
  'fragrance': '20561',
  'wallet': '2996',
  'sewing': '3118',
  'lamp': '20702',
  'light': '20702',
  'shower': '181379',
  'hiking': '181380',
  'trekking': '181380',
  'camping': '181378',
  'hammock': '181378',
  'mouse': '23160',
  'gaming': '23160',
  'chest rig': '180126',
  'tactical': '180126',
  'water bag': '181382',
  'hydration': '181382',
  'brace': '36449',
  'flosser': '31770',
  'trimmer': '31770',
  'shaver': '31770',
  'toothbrush': '31770',
  'watch': '178893',
  'wristband': '178893',
  'scrubber': '20636',
  'cleaning': '20636',
  'lunch bag': '177074',
  'cooler': '177074',
  'hair': '31413',
  'dryer': '31413',
  'straightener': '31413',
  'backpack': '169291',
  'bag': '169291',
  'purse': '169291',
  'car': '33695',
  'auto': '33695',
  'rv': '33695',
  'key': '45230',
  'keychain': '45230',
  'cap': '45230',
  'goggle': '45230',
  'scarf': '45230',
  'shawl': '45230',
  'tool': '3187',
  'gardening': '29524',
  'moss': '181036',
  'turf': '181036',
  'binoculars': '31724',
  'night vision': '31724',
  'vacuum': '20613',
  'dehumidifier': '20613',
  'heater': '20613',
  'fidget': '19016',
  'toy': '19016',
  'novelty': '19016',
  'bike': '58100',
  'horn': '58100',
  'lock': '58100',
  'earplugs': '181379',
  'file': '175685',
  'office': '175685',
  'default': '125760'
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
    department: department,
    style: style,
    power: power,
    features: features,
    mpn: `DSZ-${item.SKU}`,
    model: `DSZ-${item.SKU}`,
    itemWidth: '10 cm',
    itemHeight: '15 cm',
    bandMaterial: 'Silicone',
    caseSize: '40 mm',
    compatibleOS: 'Android / iOS'
  };
}

// 3. Process every row through all nodes
const ebayRows = [];

parsedItems.forEach((item, index) => {
  if (!item.SKU || !item.Title) return;

  const rawTitle = (item['Title'] || '').trim();
  const rawTitleLower = rawTitle.toLowerCase();
  const prohibitedTerms = ['lock picking', 'locksmith', 'gravity pick', 'lockpick', 'switchblade', 'butterfly knife', 'brass knuckles', 'taser', 'stun gun', 'replica gun'];
  if (prohibitedTerms.some(t => rawTitleLower.includes(t))) {
    console.log(`[#${index + 1}] 🚫 FILTERED PROHIBITED ITEM: ${item.SKU} (${rawTitle})`);
    return;
  }
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

  // Original Product Cost + $2.00 Fee-Buffered Formula (Direct Sourcing / Free Shipping Assumption):
  // Price = (Cost + $2.00) / (1 - 0.135)
  const flatMarkup = 2.00;
  let price = (cost + flatMarkup) / (1 - CONFIG.ebayFeeRate);
  if (price < CONFIG.minimumListingPrice) price = CONFIG.minimumListingPrice;
  if (CONFIG.charmPrice && price > 1) {
    let charm = Math.ceil(price) - 0.01;
    if (charm < price) charm += 1.00;
    price = Math.ceil(charm) - 0.01;
    if (price < CONFIG.minimumListingPrice) price = CONFIG.minimumListingPrice;
  }

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

  // Node 7: HTML Description Builder (PivotLiving Store Theme)
  const rawDesc = item['Description'] || '';
  const heroImage = imageList[0] || '';
  const galleryImg1 = imageList[1] || '';
  const galleryImg2 = imageList[2] || '';

  // Clean tracking pixels while preserving original full HTML description content & structure
  let cleanDesc = rawDesc
    .replace(/<img[^>]*dropshipzone[^>]*>/gi, '')
    .replace(/<img[^>]*logo\.png[^>]*>/gi, '')
    .replace(/<div>\s*<h2>Returns, Refunds and Replacements<\/h2>[\s\S]*?<\/div>/gi, '')
    .trim();
  if (!cleanDesc || cleanDesc.length < 20) {
    cleanDesc = `<p>${rawDesc.replace(/<[^>]+>/g, ' ').replace(/\s{2,}/g, ' ').trim()}</p>`;
  }

  const mainImageSection = heroImage ? `<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:20px;margin-bottom:24px;text-align:center;"><img src="${heroImage}" alt="${finalTitle.replace(/"/g, '&quot;')}" style="max-width:100%;max-height:480px;width:auto;height:auto;border-radius:6px;" /></div>` : '';

  let extraGallerySection = '';
  if (galleryImg1 && galleryImg2) {
    extraGallerySection = `<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:28px;"><div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:16px;text-align:center;"><img src="${galleryImg1}" alt="${finalTitle.replace(/"/g, '&quot;')}" style="max-width:100%;max-height:380px;width:auto;height:auto;border-radius:6px;" /></div><div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:16px;text-align:center;"><img src="${galleryImg2}" alt="${finalTitle.replace(/"/g, '&quot;')}" style="max-width:100%;max-height:380px;width:auto;height:auto;border-radius:6px;" /></div></div>`;
  } else if (galleryImg1) {
    extraGallerySection = `<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:20px;margin-bottom:28px;text-align:center;"><img src="${galleryImg1}" alt="${finalTitle.replace(/"/g, '&quot;')}" style="max-width:100%;max-height:450px;width:auto;height:auto;border-radius:6px;" /></div>`;
  }

  const htmlDesc = `<div style="max-width:880px;margin:0 auto;background-color:#F7F5F0;border-radius:12px;padding:28px;box-sizing:border-box;border:1px solid #E2DED4;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;"><div style="background-color:#F2EFE8;background-image:radial-gradient(#E5E0D5 1px,transparent 1px);background-size:16px 16px;border-radius:10px;padding:42px 20px 36px 20px;text-align:center;margin-bottom:28px;border:1px solid #E5E0D5;position:relative;"><a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="display:inline-block;padding:6px 20px;background-color:#FAF8F5;border-radius:20px;font-size:11px;font-weight:700;letter-spacing:2px;color:#2C3135;text-transform:uppercase;margin-bottom:14px;border:1px solid #E6D7C3;text-decoration:none;">OFFICIAL EBAY STORE &nbsp;›</a><h1 style="font-size:38px;color:#2C3135;margin:0 0 4px 0;font-weight:600;letter-spacing:-0.5px;"><a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="color:#2C3135;text-decoration:none;">Piv<span style="position:relative;display:inline-block;">o<span style="position:absolute;left:48%;top:0;bottom:0;width:1.5px;background-color:#2C3135;transform:translateX(-50%);"></span></span>tLiving</a></h1><div style="width:240px;height:1.5px;background-color:#2C3135;margin:0 auto 12px auto;"></div><p style="font-size:14px;color:#4A5056;margin:0;letter-spacing:3px;text-transform:uppercase;font-weight:500;">Modern Lifestyle Goods</p><span style="position:absolute;right:24px;bottom:18px;color:#D8D2C6;font-size:16px;">✦</span></div><div style="display:flex;flex-wrap:wrap;justify-content:space-between;background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:14px 22px;margin-bottom:28px;font-size:12px;color:#525B62;letter-spacing:0.5px;text-transform:uppercase;font-weight:600;"><div>100% Australian Stock</div><div style="color:#D2CBC0;">|</div><div>Ships in 24 Hours</div><div style="color:#D2CBC0;">|</div><div>5–10 Business Days Transit</div><div style="color:#D2CBC0;">|</div><div>High Positive Feedback</div></div><div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:26px 30px;margin-bottom:28px;"><h2 style="font-size:23px;color:#2C3135;margin:0 0 10px 0;line-height:1.35;font-weight:600;">${finalTitle}</h2><div style="font-size:12px;color:#78828A;">Item Code: <span style="color:#2C3135;font-weight:600;">DSZ-${item.SKU}</span> &nbsp;•&nbsp; Condition: <span style="color:#2C3135;font-weight:600;">Brand New In Box</span></div></div>${mainImageSection}<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:32px 34px;margin-bottom:28px;line-height:1.75;color:#383F45;font-size:14px;">${cleanDesc}</div>${extraGallerySection}<div style="background:#FFFFFF;border:1px solid #E5E0D5;border-radius:8px;padding:30px 34px;margin-bottom:28px;"><h3 style="font-size:13px;color:#78828A;margin:0 0 18px 0;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Store Commitment & Customer Care</h3><div style="margin-bottom:22px;"><h4 style="font-size:14px;color:#2C3135;margin:0 0 6px 0;font-weight:600;">100% Australian Stock — Ships in 24 Hours</h4><p style="font-size:13px;line-height:1.6;color:#525B62;margin:0;">All items are held locally in domestic Australian fulfillment centers and dispatched within 24 hours of payment clearance (Monday to Friday). Estimated delivery timeframe is <strong>5 to 10 business days</strong> nationwide, with online tracking provided immediately upon dispatch.</p></div><div style="margin-bottom:22px;"><h4 style="font-size:14px;color:#2C3135;margin:0 0 6px 0;font-weight:600;">High Positive Feedback & Quality Goods</h4><p style="font-size:13px;line-height:1.6;color:#525B62;margin:0;">At <strong>PivotLiving</strong>, we maintain a strong track record of high customer feedback by carefully selecting only reliable, high-grade products. We listen closely to buyer feedback, ensuring every item delivered to your door meets high standards of quality and dependability.</p></div><div><h4 style="font-size:14px;color:#2C3135;margin:0 0 6px 0;font-weight:600;">Dedicated Customer Service</h4><p style="font-size:13px;line-height:1.6;color:#525B62;margin:0;">We are committed to providing helpful, attentive service before and after your purchase. Have a question about this item or your order? Reach out anytime via eBay Messages and our local support team will promptly assist you.</p></div></div><div style="text-align:center;padding:18px 10px 5px 10px;font-size:12px;color:#8A949E;"><p style="margin:0 0 6px 0;font-size:14px;color:#2C3135;font-weight:600;letter-spacing:1px;text-transform:uppercase;"><a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="color:#2C3135;text-decoration:none;">PivotLiving Store</a></p><p style="margin:0 0 10px 0;">Modern Lifestyle Goods &nbsp;•&nbsp; Official eBay Australia Store</p><a href="https://www.ebay.com.au/str/pivotliving" target="_blank" style="display:inline-block;padding:8px 22px;background-color:#2C3135;color:#F7F5F0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;border-radius:4px;text-decoration:none;">Visit Our eBay Store</a></div></div>`;

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
    'C:Model': specs.model,
    'C:Type': specs.type,
    'C:Material': specs.material,
    'C:Colour': specs.colour,
    'C:Department': specs.department,
    'C:Style': specs.style,
    'C:Power Source': specs.power,
    'C:Item Width': specs.itemWidth,
    'C:Item Height': specs.itemHeight,
    'C:Band Material': specs.bandMaterial,
    'C:Case Size': specs.caseSize,
    'C:Compatible Operating System': specs.compatibleOS,
    'C:Features': specs.features,
    'C:MPN': specs.mpn,
    'Description': htmlDesc
  };

  ebayRows.push(ebayRow);
  console.log(`[#${index + 1}] ${item.SKU} | Cat: ${categoryId} | Title: ${finalTitle} (${finalTitle.length}ch) | Sell: $${finalPriceStr} | Profit: $${profitEst} (${marginPct}%)`);
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
