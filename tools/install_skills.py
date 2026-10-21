#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. mkl explicit-destination skill installer.
"""Install standalone skill directories into an explicit destination.

No personal skills directory is inferred. Existing targets are never replaced.
Omit the optional skill name to install all eight skills.
"""
import argparse
from pathlib import Path
import shutil
import sys

try:
    from .skill_payload import ROOT, build_payload, skill_names
except ImportError:
    from skill_payload import ROOT, build_payload, skill_names


def install(destination, names=None, root=ROOT):
    destination = Path(destination).expanduser().absolute()
    names = list(names) if names is not None else skill_names(root)
    if len(names) != len(set(names)):
        raise ValueError("Duplicate skill names are not allowed")
    # Validate every target and build every payload before writing any target.
    payloads = [(name, build_payload(name, root=root)) for name in names]
    for name, _ in payloads:
        target = destination / name
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Target already exists: {target}")
    destination.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for name, payload in payloads:
            target = destination / name
            target.mkdir()  # Exclusive creation also protects existing empty dirs.
            created.append(target)
            for relative, content in payload.items():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    except Exception:
        for target in reversed(created):
            shutil.rmtree(target)
        raise
    return created


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", help="skill to install (default: all)")
    parser.add_argument("--destination", required=True, type=Path, help="explicit parent directory for installed skills")
    args = parser.parse_args()
    try:
        paths = install(args.destination, [args.skill] if args.skill else None)
    except (OSError, ValueError) as error:
        parser.exit(2, f"ERROR: {error}\n")
    for path in paths:
        print(f"installed: {path}")


if __name__ == "__main__":
    main()
