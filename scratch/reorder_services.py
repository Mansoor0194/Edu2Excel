import re

def reorder_services():
    with open("services/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Find the container that holds all service items
    # We will search for all service items
    pos = 0
    items = []
    while True:
        match = re.search(r'<div[^>]*class="[^"]*service-item[^"]*"[^>]*>', html[pos:])
        if not match:
            break
        start_idx = pos + match.start()
        
        # Track div nesting
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
        title_match = re.search(r'<h3 class="elementskit-info-box-title">\s*(.*?)\s*</h3>', card_html, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        items.append({
            "title": title,
            "html": card_html,
            "start": start_idx,
            "end": end_idx
        })
        
        pos = end_idx

    print(f"Parsed {len(items)} items from services/index.html.")
    
    # Check if we parsed all 12
    if len(items) != 12:
        print("Error: Expected 12 service items, but found", len(items))
        return

    # Map cards by title (lowercased, stripped)
    card_map = {item["title"].lower().replace(" ", ""): item for item in items}
    
    # Define desired new order
    desired_order = [
        "studentvisa",
        "dependentvisa",
        "workpermit",
        "prvisa",
        "visitvisa",
        "travelandtourism",
        "educationalloan",
        "insurance",
        "simcards",
        "forex",
        "accommodation",
        "airticketbooking"
    ]
    
    # Define corrected links
    corrected_links = {
        "studentvisa": "../services/student-visa/",
        "dependentvisa": "../services/dependent-visa/",
        "workpermit": "../services/work-permit/",
        "prvisa": "../services/pr-visa/",
        "visitvisa": "../services/visit-visa/",
        "travelandtourism": "../services/travel-and-tourism/",
        "educationalloan": "../services/educational-loan/",
        "insurance": "../services/insurance/",
        "simcards": "../services/sim-cards/",
        "forex": "../services/forex/",
        "accommodation": "../services/accommodation/",
        "airticketbooking": "../services/air-ticket-booking/"
    }

    # Reorder and edit card HTMLs
    new_cards_html = []
    for idx, key in enumerate(desired_order):
        if key not in card_map:
            print(f"Error: Missing card key '{key}' in parsed cards.")
            return
        
        item = card_map[key]
        card_text = item["html"]
        
        # 1. Correct the link
        new_link = corrected_links[key]
        # Find the <a class="elementskit-btn ... href="..."> tag and update href
        card_text = re.sub(
            r'(<a\s+class="elementskit-btn[^"]*"\s+href=")[^"]*(")',
            rf'\g<1>{new_link}\g<2>',
            card_text
        )
        
        # 2. Adjust animation delay
        delay = (idx % 3) * 100
        # Check if _animation_delay exists
        if "quot;_animation_delay&quot;:" in card_text:
            if delay == 0:
                # Remove delay key
                card_text = re.sub(
                    r',&quot;_animation_delay&quot;:\d+',
                    '',
                    card_text
                )
            else:
                # Update delay key
                card_text = re.sub(
                    r'&quot;_animation_delay&quot;:\d+',
                    f'&quot;_animation_delay&quot;:{delay}',
                    card_text
                )
        else:
            if delay > 0:
                # Add delay key after _animation
                card_text = re.sub(
                    r'(&quot;_animation&quot;:&quot;[a-zA-Z]+&quot;)',
                    rf'\g<1>,&quot;_animation_delay&quot;:{delay}',
                    card_text
                )
                
        new_cards_html.append(card_text)

    # Let's join the new cards HTML
    new_grid_content = "\n\t\t\t\t".join(new_cards_html)
    
    # We will replace the entire block from the start of Card 1 to the end of Card 12
    grid_start = items[0]["start"]
    grid_end = items[-1]["end"]
    
    updated_html = html[:grid_start] + new_grid_content + html[grid_end:]
    
    with open("services/index.html", "w", encoding="utf-8") as f:
        f.write(updated_html)
        
    print("Successfully re-ordered service cards and corrected links in services/index.html!")

if __name__ == "__main__":
    reorder_services()
