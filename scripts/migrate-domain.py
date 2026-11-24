#!/usr/bin/env python3
"""Migrate the exported preview to the root of the custom domain."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
old = "/Jm-betonservice/"
count = 0
for p in root.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in {".html", ".css", ".js", ".mjs", ".json", ".xml", ".svg", ".webmanifest", ".txt"}:
        continue
    s = p.read_text(encoding="utf-8")
    # First migrate absolute URLs belonging to the former Pages host.
    t = re.sub(r"https?://dhrburgaz\.github\.io/Jm-betonservice(?=/|[\s\"'<>]|$)", "https://www.jmbetonservice.nl", s, flags=re.I)
    t = t.replace(old, "/")
    if t != s:
        p.write_text(t, encoding="utf-8")
        count += 1
if not count:
    raise RuntimeError("No preview paths migrated")
print(f"Custom-domain paths migrated in {count} files")
