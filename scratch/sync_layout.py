import os
import re
from html.parser import HTMLParser

# Helper to find matching div range by counting opening/closing div tags
def find_div_range(html, start_tag):
    start_idx = html.find(start_tag)
    if start_idx == -1:
        return None
    
    open_divs = 0
    idx = start_idx
    while idx < len(html):
        if html[idx:idx+4] == '<div':
            open_divs += 1
            idx += 4
        elif html[idx:idx+6] == '</div>' or html[idx:idx+6] == '</div\t':
            open_divs -= 1
            idx += 6
            if open_divs == 0:
                return start_idx, idx
        else:
            idx += 1
    return None

# Clean active classes from HTML string
def clean_active_classes(html_text):
    def clean_class_match(m):
        class_attr = m.group(1)
        classes = class_attr.split()
        cleaned = [c for c in classes if c not in ('current-menu-item', 'current_page_item', 'active')]
        return f'class="{" ".join(cleaned)}"'
        
    cleaned_text = re.sub(r'class="([^"]*)"', clean_class_match, html_text)
    return cleaned_text

# HTML parser to build menu tree hierarchy
class MenuParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_menu = False
        self.li_stack = []
        self.li_parents = {}
        self.href_to_li = {}
        self.id_counter = 0
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'ul' and attr_dict.get('id') == 'menu-header-menu':
            self.in_menu = True
            
        if self.in_menu:
            if tag == 'li':
                li_id = attr_dict.get('id')
                if not li_id:
                    self.id_counter += 1
                    li_id = f"auto-li-{self.id_counter}"
                if self.li_stack:
                    self.li_parents[li_id] = self.li_stack[-1]
                self.li_stack.append(li_id)
            elif tag == 'a' and self.li_stack:
                href = attr_dict.get('href')
                if href:
                    self.href_to_li[href] = self.li_stack[-1]
                    
    def handle_endtag(self, tag):
        if self.in_menu:
            if tag == 'li' and self.li_stack:
                self.li_stack.pop()
            elif tag == 'ul' and not self.li_stack:
                self.in_menu = False

def highlight_li(html_content, li_id, is_top_level):
    li_active_classes = "current-menu-item current_page_item active" if is_top_level else "active"
    
    # Target class values on <li id="li_id"> and the immediately following <a class="...">
    pattern = rf'(<li\s+id="{li_id}"[^>]*class=")([^"]*)("[^>]*>\s*<a[^>]*class=")([^"]*)(")'
    
    def repl(m):
        li_start, li_classes, middle, a_classes, end = m.groups()
        li_class_list = li_classes.split()
        for c in li_active_classes.split():
            if c not in li_class_list:
                li_class_list.append(c)
        
        a_class_list = a_classes.split()
        if "active" not in a_class_list:
            a_class_list.append("active")
            
        return f'{li_start}{" ".join(li_class_list)}{middle}{" ".join(a_class_list)}{end}'
        
    new_content, count = re.subn(pattern, repl, html_content)
    if count == 0:
        pattern_fallback = rf'(<li\s+id="{li_id}"[^>]*class=")([^"]*)(")'
        def repl_fallback(m):
            start, classes, end = m.groups()
            class_list = classes.split()
            for c in li_active_classes.split():
                if c not in class_list:
                    class_list.append(c)
            return f'{start}{" ".join(class_list)}{end}'
        new_content = re.sub(pattern_fallback, repl_fallback, html_content)
        
    return new_content

def adjust_paths(html_content, prefix):
    if prefix == './':
        return html_content
    adjusted = html_content
    adjusted = re.sub(r'href="\./', f'href="{prefix}', adjusted)
    adjusted = re.sub(r'src="\./', f'src="{prefix}', adjusted)
    adjusted = re.sub(r'srcset="\./', f'srcset="{prefix}', adjusted)
    return adjusted

def main():
    # 1. Load source templates from index.html
    with open("index.html", "r", encoding="utf-8") as f:
        homepage_html = f.read()
        
    header_start_tag = '<div class="ekit-template-content-markup ekit-template-content-header ekit-template-content-theme-support">'
    footer_start_tag = '<div class="ekit-template-content-markup ekit-template-content-footer ekit-template-content-theme-support">'
    
    hdr_range = find_div_range(homepage_html, header_start_tag)
    ftr_range = find_div_range(homepage_html, footer_start_tag)
    
    if not hdr_range or not ftr_range:
        print("Error: Could not locate header or footer block in index.html")
        return
        
    raw_header_template = homepage_html[hdr_range[0]:hdr_range[1]]
    raw_footer_template = homepage_html[ftr_range[0]:ftr_range[1]]
    
    # 2. Clean active classes from templates to create a clean base
    clean_header_template = clean_active_classes(raw_header_template)
    clean_footer_template = clean_active_classes(raw_footer_template)
    
    # 3. Parse the menu structure from the clean header template
    parser = MenuParser()
    parser.feed(clean_header_template)
    
    print(f"Header menu structure parsed: {len(parser.href_to_li)} links, {len(parser.li_parents)} hierarchy relations.")
    
    # 4. Recursively find and process all HTML files containing header/footer blocks
    updated_files_count = 0
    
    for root, dirs, files in os.walk("."):
        # Ignore common directories to speed up and prevent scanning junk
        dirs[:] = [d for d in dirs if d not in ('.git', 'scratch', 'node_modules', '.gemini')]
        
        for file in files:
            if not file.endswith(".html"):
                continue
                
            file_path = os.path.join(root, file)
            # Normalize path delimiters for windows compatibility
            norm_path = os.path.normpath(file_path).replace("\\", "/")
            
            # Remove leading './' if present
            if norm_path.startswith("./"):
                norm_path = norm_path[2:]
                
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Filter to files containing header/footer blocks
            if header_start_tag not in content or footer_start_tag not in content:
                continue
                
            # Compute path depth and prefix
            depth = norm_path.count('/')
            prefix = "./" if depth == 0 else "../" * depth
            
            # Adjust template paths for this page's directory depth
            page_header = adjust_paths(clean_header_template, prefix)
            page_footer = adjust_paths(clean_footer_template, prefix)
            
            # Identify active menu items for this page
            # We construct candidate href paths starting with "./" (as in the raw template)
            candidates = []
            parts = norm_path.split('/')
            while len(parts) >= 1:
                candidate = "./" + "/".join(parts)
                candidates.append(candidate)
                # Fallback to index.html in directory hierarchy
                if parts[-1] != 'index.html':
                    parts[-1] = 'index.html'
                else:
                    parts.pop()
            
            matched_li = None
            for cand in candidates:
                if cand in parser.href_to_li:
                    matched_li = parser.href_to_li[cand]
                    break
                    
            if matched_li:
                # Track active LI set
                active_lis = [matched_li]
                curr = matched_li
                while curr in parser.li_parents:
                    curr = parser.li_parents[curr]
                    active_lis.append(curr)
                    
                # Apply highlight classes to all active LIs in the header HTML
                for li_id in active_lis:
                    is_top_level = li_id not in parser.li_parents
                    page_header = highlight_li(page_header, li_id, is_top_level)
                    
            # Extract current page blocks and replace them
            cur_hdr_range = find_div_range(content, header_start_tag)
            
            # Note: We must locate the footer range relative to the new string since we will change the header length
            content_with_new_header = content[:cur_hdr_range[0]] + page_header + content[cur_hdr_range[1]:]
            
            cur_ftr_range = find_div_range(content_with_new_header, footer_start_tag)
            final_content = content_with_new_header[:cur_ftr_range[0]] + page_footer + content_with_new_header[cur_ftr_range[1]:]
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)
                
            updated_files_count += 1
            print(f"Synced layout: {norm_path} (depth {depth}, prefix '{prefix}', highlighted LI: {matched_li})")

    print(f"\nSuccessfully synchronized navigation header & footer layout across {updated_files_count} HTML pages!")

if __name__ == "__main__":
    main()
