import os
import sys
from datetime import datetime, timezone

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

# for each directory in the publish_dir
for dir in sorted(os.listdir(publish_dir)):
    dir_path = os.path.join(publish_dir, dir)
    print(f"{dir_path=}")
    if os.path.isdir(dir_path) and not dir.startswith('.'):
        html += f'  <h2>{dir}</h2>\n  <ul>\n'
        for file in sorted(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, file)
            print(f"{file_path=}")
            if file.endswith('.zip'):
                print(f"Found zip file: {file_path}")
                # Relative path from publish_dir directory
                rel_path = file_path.removeprefix("./gh-pages/")
                print(f"Relative path: {rel_path}")
                url = f"https://repository.kodi.reavey05.com/{rel_path}"
                html += f'    <li><a href="{url}">{file}</a></li>\n'
        html += '   </ul>\n'

html += '''
</body>
</html>'''

# write the HTML to a file
with open(os.path.join(publish_dir, 'index.html'), 'w') as f:
    f.write(html)
