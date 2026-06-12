import os
import re

workspace_dir = r"c:\Users\Manu Mansoor\Desktop\Imigo - Copy"

js_files = []
for root, dirs, files in os.walk(workspace_dir):
    if "node_modules" in root or ".claude" in root or ".vscode" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".js"):
            js_files.append(os.path.join(root, file))

print(f"Found {len(js_files)} JS files.")

keywords = [r"marquee", r"ticker", r"ekitMarqueeSwiper"]
for js_file in js_files:
    with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
            
        for kw in keywords:
            matches = list(re.finditer(kw, content, re.IGNORECASE))
            if matches:
                rel_path = os.path.relpath(js_file, workspace_dir)
                print(f"{rel_path}: found {len(matches)} matches of '{kw}'")
                for m in matches[:2]:
                    start = max(0, m.start() - 50)
                    end = min(len(content), m.end() + 100)
                    snippet = content[start:end].replace('\n', ' ')
                    print(f"  ... {snippet} ...")
