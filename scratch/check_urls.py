import re

with open('scratch/extracted_header.html', 'r', encoding='utf-8') as f:
    html = f.read()

urls = re.findall(r'(?:href|src|srcset)=\"(\./[^\"]*?)\"', html)
for url in sorted(set(urls)):
    print(url)
