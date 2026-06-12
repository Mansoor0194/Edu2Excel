import os
import re

wp_content_dir = r"c:\Users\Manu Mansoor\Desktop\Imigo - Copy\wp-content"

css_files = []
for root, dirs, files in os.walk(wp_content_dir):
    for file in files:
        if file.endswith(".css"):
            css_files.append(os.path.join(root, file))

print(f"Found {len(css_files)} CSS files.")

keywords = [r"marquee", r"ticker", r"ekitMarqueeSwiper"]
for css_file in css_files:
    with open(css_file, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
        except Exception:
            continue # Skip binary/broken encodings if any
            
        for kw in keywords:
            matches = list(re.finditer(kw, content, re.IGNORECASE))
            if matches:
                rel_path = os.path.relpath(css_file, wp_content_dir)
                print(f"{rel_path}: found {len(matches)} matches of '{kw}'")
                for m in matches[:3]:
                    start = max(0, m.start() - 60)
                    end = min(len(content), m.end() + 120)
                    snippet = content[start:end].replace('\n', ' ')
                    print(f"  ... {snippet} ...")
