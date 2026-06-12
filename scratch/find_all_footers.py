import os
import re

workspace_dir = r"c:\Users\Manu Mansoor\Desktop\Imigo - Copy"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if "node_modules" in root or ".claude" in root or ".vscode" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's extract the text under ekit-template-content-footer
    # Since we don't have bs4, we can search for class="...ekit-template-content-footer..."
    # or look for the inner content
    match = re.search(r'ekit-template-content-footer.*?class="elementor elementor-4109">(.*?)</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL | re.IGNORECASE)
    if not match:
        # Let's search by data-elementor-id="4109"
        match = re.search(r'data-elementor-id="4109"(.*?)<!-- <script type="speculationrules">', content, re.DOTALL | re.IGNORECASE)
    
    rel_path = os.path.relpath(html_file, workspace_dir)
    if match:
        footer_html = match.group(1)
        # Find some key texts like the description, headers, and copyright
        desc_match = re.search(r'<p>(Your Global Journey Starts Here.*?)</p>', footer_html, re.IGNORECASE)
        copyright_match = re.search(r'<p>(Copyright.*?)</p>', footer_html, re.IGNORECASE)
        desc_text = desc_match.group(1) if desc_match else "NOT FOUND"
        copyright_text = copyright_match.group(1) if copyright_match else "NOT FOUND"
        print(f"{rel_path}:")
        print(f"  Description: {desc_text}")
        print(f"  Copyright: {copyright_text}")
    else:
        print(f"{rel_path}: FOOTER CONTENT CONTAINER NOT FOUND")
