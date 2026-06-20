import re

with open("countries/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Parse country cards
pos = 0
items = []
while True:
    match = re.search(r'<div[^>]*class="[^"]*col-lg-2 col-md-3 col-6[^"]*"[^>]*>', html[pos:])
    if not match:
        break
    start_idx = pos + match.start()
    
    # Track div nesting to find the end of this card
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
    title_match = re.search(r'<h3>\s*(.*?)\s*</h3>', card_html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    items.append({
        "title": title,
        "start": start_idx,
        "end": end_idx,
        "html": card_html
    })
    pos = end_idx

print(f"Parsed {len(items)} country cards.")

# 2. Separate into Europe and Other Countries
europe_countries = {
    "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic", "Denmark", 
    "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", 
    "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", 
    "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovakia", 
    "Slovenia", "Spain", "Sweden", "Switzerland"
}

europe_cards = []
other_cards = []

for item in items:
    if item["title"] in europe_countries:
        europe_cards.append(item["html"])
    else:
        other_cards.append(item["html"])

print(f"Europe cards: {len(europe_cards)}, Other cards: {len(other_cards)}")

# 3. Formulate the replacement HTML
grouped_html = """
						<div class="col-md-12">
							<!-- Europe Section -->
							<div class="country-group-section">
								<h2 class="country-group-title">Europe</h2>
								<div class="row">
									""" + "\n\t\t\t\t\t\t\t\t\t".join(europe_cards) + """
								</div>
							</div>
							
							<!-- Other Countries Section -->
							<div class="country-group-section" style="margin-top: 40px;">
								<h2 class="country-group-title">Other Countries</h2>
								<div class="row">
									""" + "\n\t\t\t\t\t\t\t\t\t".join(other_cards) + """
								</div>
							</div>
						</div>
"""

# Determine the full range to replace: from the start of the first card to the end of the last card
start_pos = items[0]["start"]
end_pos = items[-1]["end"]

# Locate the containing row or adjust replacement to fit the structure
# In countries/index.html, the outer structure around cards is:
# <div class="row">
#    <div class="col-lg-2 col-md-3 col-6">... (first card)
#    ...
#    <div class="col-lg-2 col-md-3 col-6">... (last card)
#    <div class="col-md-12">... (empty pagination div or similar)
# </div>

# Let's replace the whole list of cards inside the container row
modified_html = html[:start_pos] + grouped_html + html[end_pos:]

# 4. Inject styles in <head>
style_block = """
<style>
    .country-group-title {
        font-size: 2rem;
        font-weight: 700;
        color: #002768; /* Primary blue */
        margin-top: 30px;
        margin-bottom: 20px;
        position: relative;
        padding-left: 15px;
        font-family: "Afacad Flux", sans-serif;
    }
    .country-group-title::before {
        content: "";
        position: absolute;
        left: 0;
        top: 10%;
        height: 80%;
        width: 4px;
        background-color: #BE0B32; /* Accent red */
        border-radius: 2px;
    }
    .country-group-section {
        margin-bottom: 50px;
    }
</style>
</head>"""

# Replace the first instance of </head> with the style block + </head>
modified_html = modified_html.replace("</head>", style_block, 1)

# Write out the modified HTML file
with open("countries/index.html", "w", encoding="utf-8") as f:
    f.write(modified_html)

print("countries/index.html successfully updated!")
