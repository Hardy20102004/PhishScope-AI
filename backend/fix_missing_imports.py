#!/usr/bin/env python3
"""
Fix missing typing imports (Optional, List, Dict, Any, etc.) in backend model files.
Also fixes `orm_mode` -> `from_attributes` in Pydantic v2 schema files.
"""
import os
import re

BACKEND_APP = os.path.join(os.path.dirname(__file__), "backend", "app")

TYPING_SYMBOLS = ["Optional", "List", "Dict", "Any", "Tuple", "Set", "Union", "Type"]

def fix_typing_imports(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Check which typing symbols are used but not imported
    # Find current typing import line if it exists
    typing_import_match = re.search(r"^from typing import (.+)$", content, re.MULTILINE)

    needed = []
    for sym in TYPING_SYMBOLS:
        if re.search(rf"\b{sym}\b", content):
            needed.append(sym)

    if not needed:
        return False

    if typing_import_match:
        existing_imports_str = typing_import_match.group(1)
        existing_imports = [s.strip() for s in existing_imports_str.split(",")]
        missing = [s for s in needed if s not in existing_imports]
        if not missing:
            return False
        new_imports = sorted(set(existing_imports + missing))
        new_line = f"from typing import {', '.join(new_imports)}"
        content = content.replace(typing_import_match.group(0), new_line)
    else:
        # Add typing import after the first import block
        new_line = f"from typing import {', '.join(sorted(set(needed)))}"
        # Insert after "import uuid" or at start of imports
        if "import uuid" in content:
            content = content.replace("import uuid", f"import uuid\n{new_line}", 1)
        elif "import enum" in content:
            content = content.replace("import enum", f"import enum\n{new_line}", 1)
        else:
            # Insert at top after docstring
            lines = content.split("\n")
            insert_at = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    insert_at = i
                    break
            lines.insert(insert_at, new_line)
            content = "\n".join(lines)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def fix_orm_mode(filepath: str) -> bool:
    """Fix Pydantic v1 orm_mode -> v2 from_attributes in schema files."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    content = content.replace("orm_mode = True", "from_attributes = True")
    content = content.replace("orm_mode=True", "from_attributes=True")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def scan_and_fix(directory: str, fix_func, extensions=(".py",)) -> list:
    fixed = []
    for root, dirs, files in os.walk(directory):
        # Skip virtual envs
        dirs[:] = [d for d in dirs if d not in (".venv", "__pycache__", ".git")]
        for fname in files:
            if any(fname.endswith(ext) for ext in extensions):
                fpath = os.path.join(root, fname)
                try:
                    if fix_func(fpath):
                        fixed.append(fpath.replace(BACKEND_APP, "app"))
                except Exception as e:
                    print(f"  [SKIP] {fpath}: {e}")
    return fixed


if __name__ == "__main__":
    print("=" * 60)
    print("  Fixing missing typing imports in models/...")
    print("=" * 60)
    models_dir = os.path.join(BACKEND_APP, "models")
    fixed_models = scan_and_fix(models_dir, fix_typing_imports)
    for f in fixed_models:
        print(f"  [FIXED] {f}")
    print(f"\n  Fixed {len(fixed_models)} model files.\n")

    print("=" * 60)
    print("  Fixing orm_mode -> from_attributes in schemas/...")
    print("=" * 60)
    schemas_dir = os.path.join(BACKEND_APP, "schemas")
    fixed_schemas = scan_and_fix(schemas_dir, fix_orm_mode)
    for f in fixed_schemas:
        print(f"  [FIXED] {f}")
    print(f"\n  Fixed {len(fixed_schemas)} schema files.\n")
    print("Done.")
