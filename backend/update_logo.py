import re
from pathlib import Path

p = Path("../frontend/index.html")
if not p.exists():
    p = Path("frontend/index.html")

content = p.read_text(encoding="utf-8")
pattern = r'src="data:image/[^;]+;base64,[^"]+"'
matches = re.findall(pattern, content)
print(f"Found {len(matches)} base64 logo occurrences.")

new_content = re.sub(pattern, 'src="/logo.png"', content)
p.write_text(new_content, encoding="utf-8")
print(f"Updated {p} successfully. New size: {len(new_content)} bytes.")
