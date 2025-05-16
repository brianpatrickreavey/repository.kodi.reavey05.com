import os

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>KODI Addons @ repository.kodi.reavey05.com</title>
</head>
<body>
  <h1>KODI Addons @ repository.kodi.reavey05.com</h1>'''


# if gh-pages exists
if not os.path.exists('gh-pages'):
    exit(1)
# for each directory in the gh-pages
for dir in sorted(os.listdir('gh-pages')):
    dir_path = os.path.join('gh-pages', dir)
    if os.path.isdir(dir_path) and not dir.startswith('.'):
        html += f'<h2>{dir}</h2><ul>'
        for file in sorted(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, file)
            if file.endswith('.zip'):
                # Relative path from 'gh-pages' directory
                rel_path = f"{dir}/{file}"
                html += f'<li><a href="{rel_path}">{rel_path}</a></li>'
        html += '</ul>'

html += '''
</body>
</html>'''

# write the HTML to a file
with open('gh-pages/index.html', 'w') as f:
    f.write(html)
