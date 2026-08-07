import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Fix \`${...}\` to `${...}`
    content = content.replace(r'\`', '`')
    
    # Fix organization\\'s to organization's
    content = content.replace(r"organization\\'s", r"organization\'s")

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            fix_file(os.path.join(root, file))

print("Fixed files.")
