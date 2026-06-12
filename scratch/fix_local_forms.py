import os
import re

targets = [
    'index.html',
    'our-team/index.html',
    'our-team/nia-jex/index.html',
    'our-team/devid-miller/index.html',
    'our-team/emma-sparkle/index.html',
    'our-team/alex-fresh/index.html',
    'our-team/emily-clark/index.html',
    'our-team/james-lee/index.html'
]

for filepath in targets:
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (does not exist)")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    # Clean action attributes containing #wpcf7
    content = re.sub(r'action="[^"]*?(#wpcf7-[^"]*?)"', r'action="\1"', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned form actions in {filepath}")

print("Form action cleanup complete!")
