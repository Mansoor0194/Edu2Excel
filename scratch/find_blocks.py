def find_div_range(html, start_tag):
    start_idx = html.find(start_tag)
    if start_idx == -1:
        return None
    
    # Let's count matching closing divs
    open_divs = 0
    idx = start_idx
    while idx < len(html):
        if html[idx:idx+4] == '<div':
            open_divs += 1
            idx += 4
        elif html[idx:idx+6] == '</div>' or html[idx:idx+6] == '</div\t':
            open_divs -= 1
            idx += 6
            if open_divs == 0:
                return start_idx, idx
        else:
            idx += 1
    return None

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

hdr = find_div_range(html, '<div class="ekit-template-content-markup ekit-template-content-header ekit-template-content-theme-support">')
if hdr:
    print(f"Header: {hdr[0]} to {hdr[1]}")
    # Print first few lines and last few lines
    print("Header Start:")
    print(html[hdr[0]:hdr[0]+150])
    print("...")
    print("Header End:")
    print(html[hdr[1]-150:hdr[1]])

ftr = find_div_range(html, '<div class="ekit-template-content-markup ekit-template-content-footer ekit-template-content-theme-support">')
if ftr:
    print(f"\nFooter: {ftr[0]} to {ftr[1]}")
    print("Footer Start:")
    print(html[ftr[0]:ftr[0]+150])
    print("...")
    print("Footer End:")
    print(html[ftr[1]-150:ftr[1]])
