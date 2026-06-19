with open('services/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Print lines that seem to define containers or headings
    if 'class="elementor-heading-title' in line or 'e-parent' in line:
        print(f"Line {i+1}: {line.strip()}")
