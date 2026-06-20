import os, re, glob

pages = glob.glob('**/*.html', recursive=True)[:10]

for page in pages:
    try:
        data = open(page, encoding='utf-8').read()
        ids = re.findall(r'data-elementor-id="(\d+)"', data)
        abs_count = len(re.findall(r'position.*absolute', data))
        print(f'{page}: elementor IDs={ids[:3]}, abs={abs_count}')
    except Exception as e:
        print(f'{page}: ERROR - {e}')
