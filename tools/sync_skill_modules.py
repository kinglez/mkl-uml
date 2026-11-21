#!/usr/bin/env python3
"""Synchronize checked-in copies of modules shipped with standalone skills."""
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# The first skill owns the module. Consumers ship a byte-identical copy so
# copying a skill directory works without the repository or an installer hook.
MODULES = (
    ("bce_structure.py", "mkl-uml-robustness-diagram", "mkl-pdr-review"),
    ("operation_evidence.py", "mkl-uml-design-class-model", "mkl-cdr-review"),
    ("sequence_structure.py", "mkl-uml-sequence-diagram", "mkl-cdr-review"),
)


def sync_modules(root, *, write=False):
    """Return stale copy paths. Update a stale copy only in explicit write mode."""
    stale = []
    for module, owner, consumer in MODULES:
        source = root / "skills" / owner / "scripts" / module
        target = root / "skills" / consumer / "scripts" / module
        for path in (source, target):
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"Unsafe vendored module path: {path}")
        content = source.read_bytes()
        if target.is_file() and target.read_bytes() == content:
            continue
        stale.append(target.relative_to(root))
        if write:
            target.write_bytes(content)
    return stale


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh the registered consumer copies")
    args = parser.parse_args(argv)
    try:
        stale = sync_modules(ROOT, write=args.write)
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")
    for path in stale:
        print(f"{'Updated' if args.write else 'Stale standalone module'}: {path}")
    if stale and not args.write:
        print("Run python tools/sync_skill_modules.py --write after editing the owning module.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
