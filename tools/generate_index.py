import os
import sys
from datetime import datetime, timezone

def get_category(addon):
    parts = addon.split('.')
    if len(parts) >= 2:
        prefix = parts[0]
        subtype = parts[1]
        if prefix == 'plugin':
            return f"{subtype.capitalize()} Plugins"
        elif prefix == 'script':
            return f"{subtype.capitalize()} Scripts"
        elif prefix == 'repository':
            return "Repository"
    return "Other"

publish_dir = sys.argv[1] if len(sys.argv) > 1 else 'gh-pages'
print(f"Using publish_dir: {publish_dir}")

datestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>KODI Addons @ repository.kodi.reavey05.com</title>
</head>
<body>
  <h1>KODI Addons @ repository.kodi.reavey05.com</h1>
  <p><em>Generated: {datestamp}</em></p>
'''


# if publish_dir exists
if not os.path.exists(publish_dir):
    exit(1)

# Collect all addon directories
addon_dirs = [d for d in os.listdir(publish_dir) if os.path.isdir(os.path.join(publish_dir, d)) and not d.startswith('.')]

# Group by category
addon_dict = {}
for addon in addon_dirs:
    cat = get_category(addon)
    if cat not in addon_dict:
        addon_dict[cat] = []
    addon_dict[cat].append(addon)

# Category order - collect dynamically and put Repository last
categories = sorted(set(addon_dict.keys()))
if "Repository" in categories:
    categories.remove("Repository")
    categories.append("Repository")
if "Other" in categories:
    categories.remove("Other")
    categories.append("Other")

# Generate HTML by category
for cat in categories:
    if addon_dict[cat]:
        html += f'  <h1>{cat}</h1>\n'
        for addon in sorted(addon_dict[cat]):
            dir_path = os.path.join(publish_dir, addon)
            html += f'  <h2>{addon}</h2>\n  <ul>\n'
            for file in sorted(os.listdir(dir_path)):
                file_path = os.path.join(dir_path, file)
                if file.endswith('.zip'):
                    rel_path = os.path.join(addon, file)
                    url = f"https://repository.kodi.reavey05.com/{rel_path}"
                    html += f'    <li><a href="{url}">{file}</a></li>\n'
            html += '  </ul>\n'

html += '''
</body>
</html>'''

# write the HTML to a file
with open(os.path.join(publish_dir, 'index.html'), 'w') as f:
    f.write(html)
