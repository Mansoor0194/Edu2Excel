from pathlib import Path
import re

root = Path(r'c:\Users\Manu Mansoor\Desktop\Imigo - Copy')
pattern = re.compile(
    r'(</ul>\s*\n\s*)(<li id="menu-item-3858"[^>]*>.*?<\/li>)(\s*\n\s*<div class="elementskit-nav-identity-panel")',
    re.S,
)
insert = re.compile(
    r'(<li id="menu-item-3858"[^>]*>.*?<\/li>)(\s*\n\s*<div class="elementskit-nav-identity-panel")',
    re.S,
)

count = 0
for path in sorted(root.glob('countries/*/index.html')):
    text = path.read_text(encoding='utf-8')
    new = text
    if pattern.search(new):
        new = pattern.sub(r'\2\3', new)
    if insert.search(new):
        new = insert.sub(r'\1\n                </ul>\n                \2', new)
    if new != text:
        path.write_text(new, encoding='utf-8')
        print(f'Patched: {path}')
        count += 1
print(f'Done. Patched {count} files.')
