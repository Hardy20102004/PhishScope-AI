import os
import re

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Replace `import { ... } from '../types'` with `import type { ... } from '../types'`
            new_content = re.sub(
                r'import\s+{([^}]+)}\s+from\s+[\'"]\.\./types[\'"];?',
                r'import type { \1 } from "../types";',
                content
            )
            
            # Replace `import { ... } from './types'` with `import type { ... } from './types'`
            new_content = re.sub(
                r'import\s+{([^}]+)}\s+from\s+[\'"]\./types[\'"];?',
                r'import type { \1 } from "./types";',
                new_content
            )
            
            if content != new_content:
                print(f"Fixed types in {path}")
                with open(path, 'w') as f:
                    f.write(new_content)
