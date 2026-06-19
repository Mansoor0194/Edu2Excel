import os

workspace_dir = r"c:\Users\Manu Mansoor\Desktop\Edu2Excel"
html_files = []

for root, dirs, files in os.walk(workspace_dir):
    if "node_modules" in dirs:
        dirs.remove("node_modules")
    if ".git" in dirs:
        dirs.remove(".git")
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            # check if it contains the header
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "ekit-template-content-header" in content:
                        # get relative path from workspace_dir
                        relpath = os.path.relpath(filepath, workspace_dir)
                        html_files.append(relpath)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

print(f"Found {len(html_files)} files containing header:")
for path in sorted(html_files):
    print(f"  {path}")
