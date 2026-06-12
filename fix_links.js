const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    const dirPath = path.join(dir, f);
    const isDirectory = fs.statSync(dirPath).isDirectory();
    if (isDirectory) {
      walkDir(dirPath, callback);
    } else {
      if (f.endsWith('.html')) {
        callback(dirPath);
      }
    }
  });
}

walkDir('.', (filePath) => {
  const html = fs.readFileSync(filePath, 'utf8');
  let changed = false;
  
  // Quick string replacements for the menu items, text, and URLs
  // Be careful with simple string replacements, but we know exact terms.
  
  const replacements = [
    { oldStr: 'family-visa', newStr: 'dependent-visa' },
    { oldStr: 'working-visa', newStr: 'work-permit' },
    { oldStr: 'residency-visa', newStr: 'pr-visa' },
    { oldStr: 'tourists-visa', newStr: 'visit-visa' },
    { oldStr: 'Family Visa', newStr: 'Dependent Visa' },
    { oldStr: 'Working Visa', newStr: 'Work Permit' },
    { oldStr: 'Residency Visa', newStr: 'PR Visa' },
    { oldStr: 'Tourists Visa', newStr: 'Visit Visa' },
    { oldStr: 'Tourist Visa', newStr: 'Visit Visa' },
    { oldStr: 'Family visa', newStr: 'Dependent Visa' },
    { oldStr: 'Working visa', newStr: 'Work Permit' },
    { oldStr: 'Residency visa', newStr: 'PR Visa' },
    { oldStr: 'Tourists visa', newStr: 'Visit Visa' }
  ];

  // We can use cheerio to be safer for text content and hrefs
  const $ = cheerio.load(html, { decodeEntities: false });

  $('a').each((i, el) => {
    const href = $(el).attr('href');
    if (href) {
      let newHref = href;
      newHref = newHref.replace('family-visa', 'dependent-visa');
      newHref = newHref.replace('working-visa', 'work-permit');
      newHref = newHref.replace('residency-visa', 'pr-visa');
      newHref = newHref.replace('tourists-visa', 'visit-visa');
      if (newHref !== href) {
        $(el).attr('href', newHref);
        changed = true;
      }
    }
  });

  // Update text inside elements
  $('*').contents().each(function() {
    if (this.type === 'text') {
      let text = this.data;
      let newText = text;
      // only replace exact phrases to avoid messing up classes or other attributes
      replacements.forEach(r => {
        // use regex to replace whole words/phrases case sensitive
        // actually we can just replace the strings
        if (newText.includes(r.oldStr)) {
          // ensure we don't mess up if it's already replaced, but they are distinct
          newText = newText.split(r.oldStr).join(r.newStr);
        }
      });
      if (newText !== text) {
        this.data = newText;
        changed = true;
      }
    }
  });

  if (changed) {
    fs.writeFileSync(filePath, $.html());
    console.log(`Fixed links/text in ${filePath}`);
  }
});
