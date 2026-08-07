import os

replacements = {
    r"\`\${": r"`${",
    r"}%\`": r"}%`",
    r"organization\\'s": r"organization\'s",
}

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            changed = False
            for k, v in replacements.items():
                if k in content:
                    content = content.replace(k, v)
                    changed = True
            if changed:
                print(f"Fixed {path}")
                with open(path, 'w') as f:
                    f.write(content)
