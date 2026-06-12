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

# Clean logo link in index.html if not already done
# href="./imigo" -> href="./index.html"
index_html = index_html.replace('href="./imigo"', 'href="./index.html"')

# Locate header
header_start_class = 'ekit-template-content-header'
idx_header = index_html.find(header_start_class)
if idx_header != -1:
    header_div_start = index_html.rfind('<div', 0, idx_header)
    header_end = find_matching_div(index_html, header_div_start)
    if header_end != -1:
        header_block = index_html[header_div_start:header_end]
        print(f"Extracted header length: {len(header_block)}")
        print("Header start:", header_block[:100])
        print("Header end:", header_block[-100:])
    else:
        print("Failed to find header end")
else:
    print("Failed to find header class")

# Locate footer
footer_start_class = 'ekit-template-content-footer'
idx_footer = index_html.find(footer_start_class)
if idx_footer != -1:
    footer_div_start = index_html.rfind('<div', 0, idx_footer)
    footer_end = find_matching_div(index_html, footer_div_start)
    if footer_end != -1:
        footer_block = index_html[footer_div_start:footer_end]
        print(f"Extracted footer length: {len(footer_block)}")
        print("Footer start:", footer_block[:100])
        print("Footer end:", footer_block[-100:])
    else:
        print("Failed to find footer end")
else:
    print("Failed to find footer class")
