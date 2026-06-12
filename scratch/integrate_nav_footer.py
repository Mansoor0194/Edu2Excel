import os
import re

def find_matching_div(html, start_idx):
    depth = 1
    pos = start_idx + 4
    while pos < len(html):
        m_open = re.search(r'<div\b', html[pos:], re.IGNORECASE)
        m_close = re.search(r'</div\b', html[pos:], re.IGNORECASE)
        
        if not m_close:
            return -1
            
        open_pos = pos + m_open.start() if m_open else -1
        close_pos = pos + m_close.start()
        
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            pos = open_pos + 4
        else:
            depth -= 1
            if depth == 0:
                return close_pos + 6
            pos = close_pos + 6
    return -1

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Fix logo link in homepage index.html
index_html = index_html.replace('href="./imigo"', 'href="./index.html"')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Updated logo link in index.html")

# Extract header
idx_header = index_html.find('ekit-template-content-header')
header_div_start = index_html.rfind('<div', 0, idx_header)
header_end = find_matching_div(index_html, header_div_start)
header_block = index_html[header_div_start:header_end]
print(f"Extracted header: {len(header_block)} bytes")

# Extract footer
idx_footer = index_html.find('ekit-template-content-footer')
footer_div_start = index_html.rfind('<div', 0, idx_footer)
footer_end = find_matching_div(index_html, footer_div_start)
footer_block = index_html[footer_div_start:footer_end]
print(f"Extracted footer: {len(footer_block)} bytes")

# Helper to adjust paths in header/footer block
def adjust_paths(block, prefix):
    res = block.replace('href="./', f'href="{prefix}')
    res = res.replace('src="./', f'src="{prefix}')
    return res

# List of targets
targets = [
    {
        'path': 'our-team/index.html',
        'depth': 1,
        'title': 'Our Team – Edu 2 Excel'
    },
    {
        'path': 'our-team/nia-jex/index.html',
        'depth': 2,
        'title': 'Nia Jex – Edu 2 Excel'
    },
    {
        'path': 'our-team/devid-miller/index.html',
        'depth': 2,
        'title': 'Devid Miller – Edu 2 Excel'
    },
    {
        'path': 'our-team/emma-sparkle/index.html',
        'depth': 2,
        'title': 'Emma Sparkle – Edu 2 Excel'
    },
    {
        'path': 'our-team/alex-fresh/index.html',
        'depth': 2,
        'title': 'Alex Fresh – Edu 2 Excel'
    },
    {
        'path': 'our-team/emily-clark/index.html',
        'depth': 2,
        'title': 'Emily Clark – Edu 2 Excel'
    },
    {
        'path': 'our-team/james-lee/index.html',
        'depth': 2,
        'title': 'James Lee – Edu 2 Excel'
    }
]

for t in targets:
    filepath = t['path']
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (does not exist)")
        continue
        
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    prefix = '../' if t['depth'] == 1 else '../../'
        
    # 1. Replace header
    idx = content.find('ekit-template-content-header')
    if idx != -1:
        start_div = content.rfind('<div', 0, idx)
        end_div = find_matching_div(content, start_div)
        if end_div != -1:
            new_header = adjust_paths(header_block, prefix)
            content = content[:start_div] + new_header + content[end_div:]
            print(f"- Header replaced successfully")
        else:
            print(f"- Warning: Could not find header end in {filepath}")
    else:
        print(f"- Warning: Could not find header start class in {filepath}")
        
    # 2. Replace footer
    idx = content.find('ekit-template-content-footer')
    if idx != -1:
        start_div = content.rfind('<div', 0, idx)
        end_div = find_matching_div(content, start_div)
        if end_div != -1:
            new_footer = adjust_paths(footer_block, prefix)
            content = content[:start_div] + new_footer + content[end_div:]
            print(f"- Footer replaced successfully")
        else:
            print(f"- Warning: Could not find footer end in {filepath}")
    else:
        print(f"- Warning: Could not find footer start class in {filepath}")

    # 3. Replace title tag
    content = re.sub(r'<title>.*?</title>', f"<title>{t['title']}</title>", content, flags=re.IGNORECASE)
    print(f"- Title set to '{t['title']}'")
    
    # 4. Remove WordPress bloat, speculation rules, RSD, oEmbed, shortlink, RSS feeds, emoji loader
    if t['depth'] == 2:
        # replace any demo urls
        content = content.replace('https://demo.awaikenthemes.com/imigo/', prefix)
        content = content.replace('https:\\/\\/demo.awaikenthemes.com\\/imigo\\/', prefix.replace('/', '\\/'))
        content = content.replace('https://demo.awaikenthemes.com/imigo', f'{prefix}index.html')
        content = content.replace('https:\\/\\/demo.awaikenthemes.com\\/imigo', f'{prefix.replace("/", "\\/")}index.html')
        # replace any absolute /imigo/ paths to relative paths
        content = content.replace('href="/imigo/', f'href="{prefix}')
        content = content.replace('src="/imigo/', f'src="{prefix}')
        content = content.replace('"/imigo/', f'"{prefix}')
        
        # fix form actions targeting #wpcf7
        content = re.sub(r'action="[^"]*?(#wpcf7-[^"]*?)"', r'action="\1"', content)
        
        # remove theme-panel script if present
        content = re.sub(r'<script[^>]*src="https://demo\.awaikenthemes\.com/assets/js/theme-panel\.js"[^>]*></script>', '', content)
        # remove speculation rules
        content = re.sub(r'<script type="speculationrules">.*?</script>', '', content, flags=re.DOTALL)
        # remove RSD, oEmbed, shortlink, RSS feeds, emoji styling
        content = re.sub(r'<link [^>]*?rss\+xml[^>]*?>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<link [^>]*?oembed[^>]*?>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<link [^>]*?EditURI[^>]*?>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<link [^>]*?shortlink[^>]*?>', '', content, flags=re.IGNORECASE)
        
        # remove emoji inline styles if present
        content = re.sub(r'<style id="wp-emoji-styles-inline-css">.*?</style>', '', content, flags=re.DOTALL)
        # remove emoji loader script if present
        content = re.sub(r'<script type="text/javascript">.*?wpEmojiConfig.*?</script>', '', content, flags=re.DOTALL)
        
        # clean up any consecutive blank lines
        content = re.sub(r'\n\s*\n', '\n', content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully processed and saved {filepath}\n")

print("All tasks completed!")
