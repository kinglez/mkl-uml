#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. mkl standalone skill archives.
"""Package skills/<name>/ as dist/<name>.skill ZIP archives.

Build all eight skills by default. Archives and explicit directory installs use
an identical payload, including legal notices and rewritten standalone docs.
"""
import argparse
from pathlib import Path
import zipfile

try:
    from .skill_payload import ROOT, build_payload, skill_names
except ImportError:
    from skill_payload import ROOT, build_payload, skill_names

SKILLS = ROOT / "skills"
DIST = ROOT / "dist"


def package(skill_dir: Path) -> Path:
    skill_dir = Path(skill_dir)
    root = skill_dir.parent.parent.resolve()
    payload = build_payload(skill_dir.name, root=root)
    DIST.mkdir(parents=True, exist_ok=True)
    out_path = DIST / f"{skill_dir.name}.skill"
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative, content in sorted(payload.items()):
            archive.writestr(f"{skill_dir.name}/{relative}", content)
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", help="skill to package (default: all)")
    args = parser.parse_args()
    names = [args.skill] if args.skill else skill_names()
    try:
        for name in names:
            # Validate names before constructing paths; traversal must not select
            # a similarly named directory from outside the skills root.
            build_payload(name)
        for name in names:
            print(f"packaged: {package(SKILLS / name)}")
    except (OSError, ValueError) as error:
        parser.exit(2, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
