import os
import re
from collections import defaultdict

class_pattern = re.compile(r'^class\s+([A-Za-z0-9_]+)\(Base\):')
classes = defaultdict(list)

for root, _, files in os.walk('backend/app/models'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                for line in f:
                    match = class_pattern.match(line)
                    if match:
                        classes[match.group(1)].append(path)

for cls, paths in classes.items():
    if len(paths) > 1:
        print(f"Duplicate class {cls} found in {paths}")
