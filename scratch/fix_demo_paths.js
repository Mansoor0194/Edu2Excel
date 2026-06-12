const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    if (f === 'node_modules' || f === '.git' || f === '.claude' || f === '.vscode' || f === 'scratch') return;
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

function getPrefix(filePath) {
  const rel = path.relative('.', filePath);
  const parts = rel.split(path.sep);
  const depth = parts.length - 1;
  if (depth === 0) return '.';
  return Array(depth).fill('..').join('/');
}

console.log("Starting URL and path fixing script...");

walkDir('.', (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;
  
  const prefix = getPrefix(filePath);
  const escapedPrefix = prefix.replace(/\//g, '\\/');

  // 1. Remove the theme-panel.js script tag entirely if present
  const oldLen = content.length;
  content = content.replace(/<script[^>]*src="https:\/\/demo\.awaikenthemes\.com\/assets\/js\/theme-panel\.js"[^>]*><\/script>/gi, '');
  if (content.length !== oldLen) {
    console.log(`- Removed theme-panel.js script from ${filePath}`);
  }

  // 2. Replace escaped occurrences (e.g. in JSON configs)
  let beforeEscaped = content;
  content = content.split('https:\\/\\/demo.awaikenthemes.com\\/imigo\\/').join(escapedPrefix + '\\/');
  content = content.split('https:\\/\\/demo.awaikenthemes.com\\/imigo').join(escapedPrefix);
  if (content !== beforeEscaped) {
    console.log(`- Replaced escaped demo URL in ${filePath}`);
  }

  // 3. Replace unescaped occurrences using a regex
  const regex = /https:\/\/demo\.awaikenthemes\.com\/imigo(\/[^"' \s>#]*)?/g;
  content = content.replace(regex, (match, pathPart) => {
    if (!pathPart || pathPart === '/') {
      return prefix + '/index.html';
    }
    if (pathPart.match(/\.[a-zA-Z0-9]+$/) || pathPart.startsWith('/wp-json') || pathPart.startsWith('/wp-content')) {
      return prefix + pathPart;
    }
    let cleanPath = pathPart;
    if (cleanPath.endsWith('/')) {
      cleanPath = cleanPath.slice(0, -1);
    }
    return prefix + cleanPath + '/index.html';
  });

  // 4. Update the "Our Team" navigation links in all files
  const menu3861Regex = /(<li id="menu-item-3861"[^>]*>\s*<a[^>]*href=")[^"]*("[^>]*>Our Team<\/a>)/g;
  content = content.replace(menu3861Regex, (match, p1, p2) => {
    return p1 + prefix + '/our-team/index.html' + p2;
  });

  const menu4167Regex = /(<li id="menu-item-4167"[^>]*>\s*<a[^>]*href=")[^"]*("[^>]*>Our Team<\/a>)/g;
  content = content.replace(menu4167Regex, (match, p1, p2) => {
    return p1 + prefix + '/our-team/index.html' + p2;
  });

  // 5. Update "Team Details" navigation links in all files
  const menu3864Regex = /(<li id="menu-item-3864"[^>]*>\s*<a[^>]*href=")[^"]*("[^>]*>Team Details<\/a>)/g;
  content = content.replace(menu3864Regex, (match, p1, p2) => {
    return p1 + prefix + '/our-team/nia-jex/index.html' + p2;
  });

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Successfully updated: ${filePath}`);
  }
});

console.log("Done fixing URLs!");
