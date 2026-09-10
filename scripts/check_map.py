#!/usr/bin/env python3
"""Check a flat concept map using plain [[name]] links; no dependencies."""

import argparse
import re
from collections import deque
from pathlib import Path


def prose(text):
    """Remove fenced and inline code so examples do not become graph edges."""
    lines = []
    fence_char = None
    fence_size = 0
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence_char is None:
                fence_char, fence_size = marker[0], len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_size and not tail.strip():
                fence_char = None
                continue
        if fence_char is None:
            lines.append(line)
    return re.sub(r"(`+)(?!`)(.*?)\1(?!`)", "", "\n".join(lines), flags=re.S)


def check(directory):
    if not directory.is_dir():
        return [f"マップのディレクトリがありません: {directory}"], None, 0, 0

    errors = []
    for path in sorted(directory.rglob("*.md")):
        relative = path.relative_to(directory)
        if len(relative.parts) > 1 and not any(p.startswith(".") for p in relative.parts):
            errors.append(f"Markdown は直下に置いてください: {relative}")

    files = {p.stem: p for p in sorted(directory.glob("*.md")) if not p.name.startswith(".")}
    if not files:
        return errors + ["ノードとなる Markdown ファイルがありません"], None, 0, 0

    children = {name: set() for name in files}
    parents = {name: set() for name in files}
    for name, path in files.items():
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path.name} を読めません: {exc}")
            continue
        for target in sorted(set(re.findall(r"\[\[([^\]\n]*)\]\]", prose(content)))):
            if not target or any(c in target for c in "|#/\\"):
                errors.append(f"{path.name}: 直下のファイル名を使う [[名前]] の形にしてください: [[{target}]]")
            elif target not in files:
                errors.append(f"リンク切れ: {path.name} → {target}.md")
            else:
                children[name].add(target)
                parents[target].add(name)

    roots = sorted(name for name in files if not parents[name])
    root = roots[0] if len(roots) == 1 else None
    if root is None:
        errors.append(f"root は一つ必要です（現在 {len(roots)} 個）: {', '.join(roots) or 'なし'}")
    for name in sorted(files):
        if len(parents[name]) > 1:
            errors.append(f"親が複数: {name} ← {', '.join(sorted(parents[name]))}")

    if root is not None:
        reached, todo = set(), [root]
        while todo:
            name = todo.pop()
            if name not in reached:
                reached.add(name)
                todo.extend(children[name])
        if reached != set(files):
            errors.append(f"{root} から到達できません: {', '.join(sorted(set(files) - reached))}")

    # Topological removal detects cycles even in components disconnected from root.
    remaining = {name: len(parents[name]) for name in files}
    ready = deque(roots)
    removed = 0
    while ready:
        name = ready.popleft()
        removed += 1
        for child in sorted(children[name]):
            remaining[child] -= 1
            if remaining[child] == 0:
                ready.append(child)
    if removed != len(files):
        errors.append("循環があります")

    edges = sum(len(targets) for targets in children.values())
    return errors, root, len(files), edges


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map_dir", type=Path, help="対象の docs/map/ ディレクトリ")
    args = parser.parse_args()
    errors, root, nodes, edges = check(args.map_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: root={root}, nodes={nodes}, edges={edges}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
