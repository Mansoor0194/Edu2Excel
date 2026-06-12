filepath = r"c:\Users\Manu Mansoor\Desktop\Imigo - Copy\wp-content\plugins\elementskit\widgets\init\assets\css\widget-styles-pro.css"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for keyframes for ticker-left
import re
matches = [m.start() for m in re.finditer(r'@keyframes', content, re.IGNORECASE)]
print(f"Found {len(matches)} keyframes definitions.")

# Print sections around "ticker-left"
ticker_matches = [m.start() for m in re.finditer(r'ticker-left', content, re.IGNORECASE)]
print(f"Found {len(ticker_matches)} occurrences of 'ticker-left'.")
for idx, m in enumerate(ticker_matches[:5]):
    start = max(0, m - 100)
    end = min(len(content), m + 200)
    snippet = content[start:end].replace('\n', ' ')
    print(f"Match {idx+1}: ... {snippet} ...")
