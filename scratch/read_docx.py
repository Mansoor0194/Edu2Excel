import zipfile
import xml.etree.ElementTree as ET
import os

target_dir = r"c:\Users\Manu Mansoor\Desktop\Imigo - Copy"

def get_docx_text(path):
    if not os.path.exists(path):
        return f"File not found: {path}"
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            paragraphs = []
            for paragraph in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                texts = [node.text for node in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                if texts:
                    paragraphs.append("".join(texts))
            return "\n".join(paragraphs)
    except Exception as e:
        return f"Error reading {path}: {e}"

docx_files = ["Crucial Missing Content.docx", "EDU2EXCEL @ About Us.docx", "Website Content.docx"]

output_path = os.path.join(target_dir, "scratch", "extracted_content.txt")
with open(output_path, "w", encoding="utf-8") as out:
    for f in docx_files:
        full_path = os.path.join(target_dir, f)
        out.write("=" * 60 + "\n")
        out.write(f"File: {f}\n")
        out.write("=" * 60 + "\n")
        text = get_docx_text(full_path)
        out.write(text + "\n\n")

print(f"Extracted content written to {output_path}")
