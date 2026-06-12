import urllib.request
import os

css_files = [
    "post-11317.css",
    "post-11318.css",
    "post-11319.css",
    "post-11320.css",
    "post-11321.css"
]

base_url = "https://demo.awaikenthemes.com/imigo/wp-content/uploads/elementor/css/"
local_dir = "wp-content/uploads/elementor/css/"

os.makedirs(local_dir, exist_ok=True)

for css_file in css_files:
    url = base_url + css_file
    local_path = os.path.join(local_dir, css_file)
    print(f"Downloading {url} -> {local_path} ...")
    try:
        urllib.request.urlretrieve(url, local_path)
        print("Success!")
    except Exception as e:
        print(f"Error downloading {css_file}: {e}")
