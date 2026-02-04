import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def get_category_info(addon):
    parts = addon.split('.')
    if len(parts) >= 2:
        prefix = parts[0]
        subtype = parts[1]
        if prefix in ['plugin', 'script']:
            main_type = f"{prefix.capitalize()}s"  # Plugins, Scripts
            sub_type = f"{subtype.capitalize()} {prefix.capitalize()}s"  # Video Plugins, Module Scripts
            return main_type, sub_type
        elif prefix == 'repository':
            return "Repository", "Repository"
    return "Other", "Other"

def get_metadata(addon_dir):
    addon_xml = os.path.join(addon_dir, 'addon.xml')
    print(f"Checking {addon_xml}")
    metadata = {'description': '', 'news': ''}
    if os.path.exists(addon_xml):
        print(f"File exists")
        tree = ET.parse(addon_xml)
        root = tree.getroot()
        print(f"Root tag: {root.tag}")
        
        # Find the metadata extension
        metadata_ext = root.find('extension[@point="xbmc.addon.metadata"]')
        if metadata_ext is not None:
            desc_elem = metadata_ext.find('description')
            if desc_elem is not None:
                metadata['description'] = desc_elem.text or ""
                print(f"Description element found: {repr(metadata['description'])}")
            else:
                print("No description element in metadata extension")
            
            news_elem = metadata_ext.find('news')
            if news_elem is not None:
                metadata['news'] = news_elem.text or ""
                print(f"News element found: {repr(metadata['news'])}")
            else:
                print("No news element in metadata extension")
        else:
            print("No metadata extension found")
    else:
        print("File does not exist")
    return metadata

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

# Group by main type and sub type
main_dict = {}
for addon in addon_dirs:
    main_type, sub_type = get_category_info(addon)
    if main_type not in main_dict:
        main_dict[main_type] = {}
    if sub_type not in main_dict[main_type]:
        main_dict[main_type][sub_type] = []
    main_dict[main_type][sub_type].append(addon)

# Main type order
main_order = ["Plugins", "Scripts", "Repository", "Other"]

# Generate HTML by main type, then sub type
for main in main_order:
    if main in main_dict:
        html += f'  <h1>{main}</h1>\n'
        for sub in sorted(main_dict[main].keys()):
            html += f'  <h2>{sub}</h2>\n'
            for addon in sorted(main_dict[main][sub]):
                dir_path = os.path.join(publish_dir, addon)
                metadata = get_metadata(dir_path)
                desc = metadata['description']
                news = metadata['news']
                print(f"For {addon}, desc: {repr(desc)}, news: {repr(news)}")
                html += f'  <h3>{addon}</h3>\n'
                if desc:
                    html += f'  <p>Description: {desc}</p>\n'
                if news:
                    html += f'  <p>Latest News: {news}</p>\n'
                for file in sorted(os.listdir(dir_path)):
                    file_path = os.path.join(dir_path, file)
                    if file.endswith('.zip'):
                        rel_path = os.path.join(addon, file)
                        url = f"https://repository.kodi.reavey05.com/{rel_path}"
                        html += f'  <p>ZIP Link: <a href="{url}">{file}</a></p>\n'

html += '''
</body>
</html>'''

# write the HTML to a file
with open(os.path.join(publish_dir, 'index.html'), 'w') as f:
    f.write(html)
