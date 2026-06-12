import os

def clean_css_file(filepath):
    # Determine depth relative to root
    # wp-content/uploads/elementor/css/post-11317.css is at depth 4
    # We can compute depth based on path separators
    relpath = os.path.relpath(filepath, '.')
    parts = relpath.split(os.sep)
    depth = len(parts) - 1
    prefix = '/'.join(['..'] * depth) + '/'
    escaped_prefix = '\\/'.join(['..'] * depth) + '\\/'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace('https://demo.awaikenthemes.com/imigo/', prefix)
    content = content.replace('https:\\/\\/demo.awaikenthemes.com\\/imigo\\/', escaped_prefix)
    content = content.replace('https://demo.awaikenthemes.com/imigo', prefix[:-1])
    content = content.replace('https:\\/\\/demo.awaikenthemes.com\\/imigo', escaped_prefix[:-2])

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned CSS paths in {filepath} (depth {depth})")

# Walk through wp-content and clean all css files
for root, dirs, files in os.walk('wp-content'):
    for file in files:
        if file.endswith('.css'):
            clean_css_file(os.path.join(root, file))

print("CSS cleanup complete!")
