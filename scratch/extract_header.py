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

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

idx_header = index_html.find('ekit-template-content-header')
header_div_start = index_html.rfind('<div', 0, idx_header)
header_end = find_matching_div(index_html, header_div_start)
header_block = index_html[header_div_start:header_end]

with open('scratch/extracted_header.html', 'w', encoding='utf-8') as f:
    f.write(header_block)

print(f"Extracted header block of size {len(header_block)} bytes saved to scratch/extracted_header.html")
