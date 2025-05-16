import os


html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>KODI Addons @ reavey05.com</title>
  <style>
    body { font-family: sans-serif; margin: 2em; }
    h1 { font-size: 1.5em; }
    ul { list-style: none; padding: 0; }
    li { margin: 0.5em 0; }
    a { text-decoration: none; color: #0366d6; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>Addons:</h1>'''

# for each directory in the current directory listing
for dir in sorted(os.listdir('.')):
    if os.path.isdir(dir):
        html += f'<h2>{dir}</h2><ul>'
        # for each file in the directory
        for file in sorted(os.listdir(dir)):
            # if the file is a .zip file
            if file.endswith('.zip'):
                # add a link to the file
                html += f'<li><a href="{dir}/{file}">{file}</a></li>'
        html += '</ul>'

html += '''
</body>
</html>'''

# write the HTML to a file
with open('gh-pages/index.html', 'w') as f:
    f.write(html)
