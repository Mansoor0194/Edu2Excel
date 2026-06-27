import html.parser

class HTMLValidator(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        
    def handle_starttag(self, tag, attrs):
        # List of self-closing tags
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link', 'col', 'base']:
            self.tags.append((tag, self.getpos()))
            
    def handle_endtag(self, tag):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link', 'col', 'base']:
            if not self.tags:
                print(f"Error: Closed tag '{tag}' at position {self.getpos()} but tag stack is empty.")
                return
            expected_tag, pos = self.tags.pop()
            if tag != expected_tag:
                print(f"Error: Closed tag '{tag}' at position {self.getpos()} but expected '{expected_tag}' opened at {pos}.")

validator = HTMLValidator()
with open("events/index.html", "r", encoding="utf-8") as f:
    content = f.read()

try:
    validator.feed(content)
    if validator.tags:
        print("Warning: Unclosed tags left in stack:")
        for t, pos in validator.tags:
            print(f"  Tag '{t}' opened at {pos}")
    else:
        print("HTML is structured correctly with no dangling tags!")
except Exception as e:
    print(f"Parsing error: {e}")
