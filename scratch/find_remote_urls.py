import os
import re

remote_urls = set()
url_pattern = re.compile(r'https://demo\.awaikenthemes\.com/[^\s"\'\)>#]+')

for root, dirs, files in os.walk('our-team'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = url_pattern.findall(content)
                for match in matches:
                    remote_urls.add(match)

print(f"Found {len(remote_urls)} unique remote URLs:")
for url in sorted(remote_urls):
    print(url)
