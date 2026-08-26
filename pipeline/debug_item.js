const fs = require('fs');
const path = require('path');

const content = fs.readFileSync(path.join(__dirname, '..', 'sample_dropshipzone_input.csv'), 'utf8');

const parsed = [];
let curCell = '';
let curRow = [];
let insideQuotes = false;
for (let i = 0; i < content.length; i++) {
  const c = content[i];
  if (c === '"') {
    if (insideQuotes && content[i+1] === '"') { curCell += '"'; i++; }
    else { insideQuotes = !insideQuotes; }
  } else if (c === ',' && !insideQuotes) {
    curRow.push(curCell.trim()); curCell = '';
  } else if ((c === '\n' || c === '\r') && !insideQuotes) {
    if (c === '\r' && content[i+1] === '\n') i++;
    curRow.push(curCell.trim()); curCell = '';
    if (curRow.some(cell => cell.length > 0)) parsed.push(curRow);
    curRow = [];
  } else {
    curCell += c;
  }
}
if (curRow.some(cell => cell.length > 0)) parsed.push(curRow);

const headers = parsed[0];
const itemRow = parsed.find(r => r[0] === 'V888-ELOSUNG12212');
console.log('=== Raw Supplier Data for V888-ELOSUNG12212 ===');
headers.forEach((h, idx) => {
  if (itemRow && itemRow[idx]) {
    if (h !== 'Description') console.log(`${h}: ${itemRow[idx]}`);
  }
});
