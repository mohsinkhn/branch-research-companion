#!/usr/bin/env python3
"""
Architecture Documentation Generator

This script generates and updates architecture documentation including:
- Module structure and hierarchy
- Dependency graphs
- Code metrics
- File inventory

Run with: uv run python scripts/generate_arch_docs.py
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src" / "branch"
DOCS_DIR = PROJECT_ROOT / "docs"
ARCH_DIR = DOCS_DIR / "architecture"


def ensure_dirs() -> None:
    """Ensure required directories exist."""
    ARCH_DIR.mkdir(parents=True, exist_ok=True)


def get_python_files(directory: Path) -> list[Path]:
    """Get all Python files in a directory recursively."""
    return list(directory.rglob("*.py"))


def parse_module_info(file_path: Path) -> dict[str, Any]:
    """Parse a Python file and extract module information."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        info: dict[str, Any] = {
            "path": str(file_path.relative_to(PROJECT_ROOT)),
            "classes": [],
            "functions": [],
            "imports": [],
            "docstring": ast.get_docstring(tree) or "",
            "lines": len(content.splitlines()),
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [
                        m.name for m in node.body if isinstance(m, ast.FunctionDef)
                    ],
                    "docstring": ast.get_docstring(node) or "",
                    "line": node.lineno,
                }
                info["classes"].append(class_info)

            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                # Only top-level functions
                func_info = {
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "",
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                }
                info["functions"].append(func_info)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    info["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    info["imports"].append(node.module)

        return info

    except SyntaxError as e:
        return {
            "path": str(file_path.relative_to(PROJECT_ROOT)),
            "error": f"Syntax error: {e}",
        }


def analyze_dependencies(modules: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Analyze dependencies between modules."""
    deps: dict[str, list[str]] = defaultdict(list)

    for module in modules:
        module_name = module["path"].replace("/", ".").replace(".py", "")
        if module_name.endswith(".__init__"):
            module_name = module_name[:-9]

        for imp in module.get("imports", []):
            if imp.startswith("branch"):
                deps[module_name].append(imp)

    return dict(deps)


def generate_file_tree(directory: Path, prefix: str = "") -> str:
    """Generate a text-based file tree."""
    lines = []
    entries = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        current_prefix = "└── " if is_last else "├── "
        next_prefix = "    " if is_last else "│   "

        if entry.name.startswith(".") or entry.name == "__pycache__":
            continue

        if entry.is_dir():
            lines.append(f"{prefix}{current_prefix}{entry.name}/")
            lines.append(generate_file_tree(entry, prefix + next_prefix))
        else:
            lines.append(f"{prefix}{current_prefix}{entry.name}")

    return "\n".join(filter(None, lines))


def generate_module_inventory(modules: list[dict[str, Any]]) -> str:
    """Generate a markdown table of all modules."""
    lines = [
        "| File | Lines | Classes | Functions | Description |",
        "|------|-------|---------|-----------|-------------|",
    ]

    for module in sorted(modules, key=lambda x: x["path"]):
        if "error" in module:
            continue

        path = module["path"]
        loc = module["lines"]
        classes = ", ".join(c["name"] for c in module["classes"]) or "-"
        functions = ", ".join(f["name"] for f in module["functions"]) or "-"
        desc = module["docstring"].split("\n")[0][:50] if module["docstring"] else "-"

        lines.append(f"| `{path}` | {loc} | {classes} | {functions} | {desc} |")

    return "\n".join(lines)


def generate_class_hierarchy(modules: list[dict[str, Any]]) -> str:
    """Generate a class hierarchy overview."""
    lines = ["## Class Hierarchy\n"]

    for module in sorted(modules, key=lambda x: x["path"]):
        if "error" in module or not module["classes"]:
            continue

        lines.append(f"### `{module['path']}`\n")

        for cls in module["classes"]:
            lines.append(f"**{cls['name']}** (line {cls['line']})")
            if cls["docstring"]:
                lines.append(f"> {cls['docstring'].split(chr(10))[0]}")
            if cls["methods"]:
                lines.append(f"- Methods: `{'`, `'.join(cls['methods'])}`")
            lines.append("")

    return "\n".join(lines)


def run_code_metrics() -> dict[str, Any]:
    """Run radon to get code metrics (if available)."""
    metrics = {}

    try:
        # Cyclomatic complexity
        result = subprocess.run(
            ["uv", "run", "radon", "cc", str(SRC_DIR), "-a", "-j"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            metrics["complexity"] = json.loads(result.stdout)

        # Maintainability index
        result = subprocess.run(
            ["uv", "run", "radon", "mi", str(SRC_DIR), "-j"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            metrics["maintainability"] = json.loads(result.stdout)

    except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
        # radon not installed or other error
        pass

    return metrics


def generate_architecture_doc(
    modules: list[dict[str, Any]], deps: dict[str, list[str]]
) -> str:
    """Generate the main architecture documentation."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    doc = f"""# Code Architecture - Auto-Generated

> **Generated:** {timestamp}
> **Generator:** `scripts/generate_arch_docs.py`

This document is automatically generated. Do not edit manually.
For the human-maintained architecture guide, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## File Tree

```
{generate_file_tree(SRC_DIR)}
```

---

## Module Inventory

{generate_module_inventory(modules)}

---

{generate_class_hierarchy(modules)}

---

## Internal Dependencies

```
"""

    for module, imports in sorted(deps.items()):
        if imports:
            doc += f"{module}\n"
            for imp in imports:
                doc += f"  └── {imp}\n"

    doc += """```

---

## Metrics Summary

Run `uv run radon cc src/branch -a` for complexity metrics.
Run `uv run radon mi src/branch` for maintainability index.

---

*This file is auto-generated. Run `uv run python scripts/generate_arch_docs.py` to update.*
"""

    return doc


def generate_json_structure(
    modules: list[dict[str, Any]], deps: dict[str, list[str]]
) -> dict[str, Any]:
    """Generate a JSON structure of the codebase for tooling."""
    return {
        "generated_at": datetime.now().isoformat(),
        "project": "branch-research-companion",
        "modules": modules,
        "dependencies": deps,
        "stats": {
            "total_files": len(modules),
            "total_lines": sum(m.get("lines", 0) for m in modules),
            "total_classes": sum(len(m.get("classes", [])) for m in modules),
            "total_functions": sum(len(m.get("functions", [])) for m in modules),
        },
    }


def main() -> int:
    """Main entry point."""
    print("🔍 Analyzing codebase...")

    ensure_dirs()

    # Parse all Python files
    python_files = get_python_files(SRC_DIR)
    modules = [parse_module_info(f) for f in python_files]

    print(f"   Found {len(modules)} Python files")

    # Analyze dependencies
    deps = analyze_dependencies(modules)
    print(f"   Found {len(deps)} modules with internal dependencies")

    # Generate documentation
    print("📝 Generating documentation...")

    # Main architecture doc (auto-generated)
    arch_doc = generate_architecture_doc(modules, deps)
    arch_file = ARCH_DIR / "CODE_STRUCTURE.md"
    arch_file.write_text(arch_doc)
    print(f"   Written: {arch_file}")

    # JSON structure for tooling
    json_structure = generate_json_structure(modules, deps)
    json_file = ARCH_DIR / "structure.json"
    json_file.write_text(json.dumps(json_structure, indent=2))
    print(f"   Written: {json_file}")

    print("✅ Architecture documentation generated!")
    print(f"\n📂 Output directory: {ARCH_DIR}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
