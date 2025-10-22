#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_readmes.py

Scans an organization workspace (root directory), generates directory trees,
and injects/updates an "Appendix: Directory Structure" section in each repo's README.md.
Also writes/updates .github/README.md at the org root with the overall structure.

Usage:
  python3 update_readmes.py --root "/home/you/projects/comics-lab" [--max-depth 4] [--exclude ".venv,.git,__pycache__"] [--dry-run]
"""
import argparse, os, sys, re
from pathlib import Path
from typing import List, Set

BEGIN_MARKER = "<!-- BEGIN DIR TREE -->"
END_MARKER   = "<!-- END DIR TREE -->"

def should_skip(name: str, exclude: Set[str]) -> bool:
    return name in exclude or name.startswith(".git")

def render_tree(root: Path, max_depth: int, exclude: Set[str]) -> str:
    lines: List[str] = []
    prefix_stack: List[str] = []
    def walk(dir_path: Path, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted([e for e in dir_path.iterdir()], key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return
        for i, entry in enumerate(entries):
            name = entry.name
            if should_skip(name, exclude):
                continue
            connector = "└── " if i == len(entries) - 1 else "├── "
            lines.append("".join(prefix_stack) + connector + name)
            if entry.is_dir():
                prefix_stack.append("    " if i == len(entries) - 1 else "│   ")
                walk(entry, depth + 1)
                prefix_stack.pop()
    lines.append(root.name)
    walk(root, 1)
    return "```\n" + "\n".join(lines) + "\n```"

def upsert_appendix(readme_text: str, title: str, tree_md: str) -> str:
    appendix = f"\n\n## Appendix: Directory Structure — {title}\n\n{BEGIN_MARKER}\n{tree_md}\n{END_MARKER}\n"
    pattern = re.compile(
        r"## Appendix: Directory Structure — .*?\n\n" + re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER) + r"\n?",
        flags=re.DOTALL | re.IGNORECASE,
    )
    if pattern.search(readme_text):
        return pattern.sub(appendix.strip() + "\n", readme_text)
    else:
        return readme_text.rstrip() + appendix

def ensure_readme(repo_dir: Path) -> Path:
    rd = repo_dir / "README.md"
    if not rd.exists():
        rd.write_text(f"# {repo_dir.name}\n\n_Auto-generated README stub. Update this content as needed._\n", encoding="utf-8")
    return rd

def update_repo_readme(repo_dir: Path, max_depth: int, exclude: Set[str], dry_run: bool=False) -> bool:
    readme_path = ensure_readme(repo_dir)
    title = repo_dir.name
    tree_md = render_tree(repo_dir, max_depth, exclude)
    current = readme_path.read_text(encoding="utf-8", errors="ignore")
    updated = upsert_appendix(current, title, tree_md)
    if updated != current:
        if not dry_run:
            readme_path.write_text(updated, encoding="utf-8")
        return True
    return False

def update_org_readme(org_root: Path, max_depth: int, exclude: Set[str], dry_run: bool=False) -> bool:
    gh_dir = org_root / ".github"
    gh_dir.mkdir(parents=True, exist_ok=True)
    readme = gh_dir / "README.md"
    header = "# comics-lab — Organization Overview\n\nThis README describes the overall directory structure of the organization workspace.\n\n"
    tree_md = render_tree(org_root, max_depth, exclude)
    block = f"## Appendix: Overall Organization Directory Structure\n\n{BEGIN_MARKER}\n{tree_md}\n{END_MARKER}\n"
    new_text = header + block
    if readme.exists():
        current = readme.read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(
            r"## Appendix: Overall Organization Directory Structure\n\n" + re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER) + r"\n?",
            flags=re.DOTALL | re.IGNORECASE,
        )
        if pattern.search(current):
            merged = pattern.sub(block, current)
        else:
            merged = current.rstrip() + "\n\n" + block
        if merged != current and not dry_run:
            readme.write_text(merged, encoding="utf-8")
            return True
        return False
    else:
        if not dry_run:
            readme.write_text(new_text, encoding="utf-8")
        return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path, help="Organization root directory (e.g., /home/you/projects/comics-lab)")
    ap.add_argument("--max-depth", type=int, default=4, help="Max depth for generated trees (default: 4)")
    ap.add_argument("--exclude", type=str, default=".git,.venv,__pycache__,.pytest_cache,.mypy_cache", help="Comma-separated names to exclude")
    ap.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    args = ap.parse_args()

    root: Path = args.root.expanduser().resolve()
    if not root.exists():
        print(f"[ERROR] Root does not exist: {root}")
        sys.exit(2)

    exclude: Set[str] = set(x.strip() for x in args.exclude.split(",") if x.strip())

    repos = [p for p in root.iterdir() if p.is_dir() and not should_skip(p.name, exclude) and p.name != ".github"]
    changed = 0

    print(f"[INFO] Root: {root}")
    print(f"[INFO] Repos: {[p.name for p in repos]}")
    print(f"[INFO] Exclude: {sorted(exclude)}")
    print(f"[INFO] Max depth: {args.max_depth}")
    print(f"[INFO] Dry run: {args.dry_run}")

    for repo in repos:
        did = update_repo_readme(repo, args.max_depth, exclude, dry_run=args.dry_run)
        print(f"[{'DRY' if args.dry_run else 'WRITE'}] {repo.name} README {'updated' if did else 'unchanged'}")
        changed += int(did)

    did_org = update_org_readme(root, args.max_depth, exclude, dry_run=args.dry_run)
    print(f"[{'DRY' if args.dry_run else 'WRITE'}] .github/README.md {'updated' if did_org else 'unchanged'}")
    changed += int(did_org)

    print(f"[DONE] Files changed: {changed}")
    sys.exit(0)

if __name__ == "__main__":
    main()
