import re

with open('scratch/extracted_header.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all href/src attributes that don't start with ./
attrs = re.findall(r'(?:href|src|srcset)=\"((?!\./)[^\"]*?)\"', html)
for attr in sorted(set(attrs)):
    print(attr)
