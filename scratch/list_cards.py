import re

with open("services/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Service items are defined by elements with class "service-item"
# Let's find each div that has class "service-item" and count their tags to extract them fully.
items = []
pos = 0
while True:
    match = re.search(r'<div[^>]*class="[^"]*service-item[^"]*"[^>]*>', html[pos:])
    if not match:
        break
    start_idx = pos + match.start()
    
    # Track div nesting to find the matching closing div
    open_divs = 0
    end_idx = start_idx
    while end_idx < len(html):
        if html[end_idx:end_idx+4] == '<div':
            open_divs += 1
            end_idx += 4
        elif html[end_idx:end_idx+6] == '</div\t' or html[end_idx:end_idx+6] == '</div>':
            open_divs -= 1
            end_idx += 6
            if open_divs == 0:
                break
        else:
            end_idx += 1
            
    card_html = html[start_idx:end_idx]
    
    # Extract title
    title_match = re.search(r'<h3 class="elementskit-info-box-title">\s*(.*?)\s*</h3>', card_html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    # Extract button href
    href_match = re.search(r'href="([^"]*)"', card_html)
    href = href_match.group(1) if href_match else "None"
    
    items.append({
        "title": title,
        "href": href,
        "start": start_idx,
        "end": end_idx,
        "html": card_html
    })
    
    pos = end_idx

print(f"Found {len(items)} service items:")
for i, item in enumerate(items):
    print(f"{i+1}. Title: {item['title']} | Href: {item['href']} | Range: {item['start']}-{item['end']}")
