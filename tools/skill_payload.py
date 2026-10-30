#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. mkl standalone skill payloads.
"""Build the same self-contained file payload for ZIP and directory installs."""
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ("README.md", "BIBLIOGRAPHY.md", "THIRD_PARTY_SOURCES.md", "RELEASE_NOTES.md", "MKL_METHODOLOGY.md", "OPERATING_CONTRACT.md", "INSTALLATION.md", "EXAMPLES.md", "VALIDATION.md")
EXCLUDED = {"__pycache__", ".DS_Store", "Thumbs.db", ".git", ".pytest_cache"}
LINK = re.compile(r"(?P<label>!?\[[^\]\n]*\])\((?P<target><[^>\n]+>|[^\s)]+)(?P<title>\s+[^)]+)?\)")
# Also handles the outer destination in nested Markdown badges.
DESTINATION = re.compile(r"(?<=\]\()(?P<target><[^>\n]+>|[^\s)]+)(?=\s|\))")


def skill_names(root=ROOT):
    return sorted(path.name for path in (Path(root) / "skills").iterdir()
                  if path.is_dir() and not path.name.startswith("."))


def _safe_skill(name, root):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"Invalid skill name: {name!r}")
    directory = root / "skills" / name
    if (directory.is_symlink() or not directory.resolve().is_relative_to(root / "skills")
            or not directory.is_dir() or not (directory / "SKILL.md").is_file()):
        raise ValueError(f"Unknown or unsafe skill: {name}")
    return directory


def _rewrite_markdown(text, source, output, sources):
    def target_for(destination):
        url = urlsplit(destination.strip("<>"))
        if url.scheme or url.netloc or not url.path:
            return destination
        resolved = (source.parent / unquote(url.path)).resolve()
        mapped = sources.get(resolved)
        if mapped is None:
            # Directories are valid links when they contain payload files.
            descendants = [(src, dst) for src, dst in sources.items() if resolved in src.parents]
            if descendants:
                src, dst = descendants[0]
                mapped = dst
                for _ in src.relative_to(resolved).parts:
                    mapped = mapped.parent
        if mapped is None:
            return None
        relative = Path(os.path.relpath(mapped, output.parent)).as_posix()
        return relative + ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")

    def replace_link(match):
        destination = target_for(match.group("target"))
        if destination is None:
            # Repository-only material stays readable but is not a broken link
            # to a sibling package or a path outside this standalone skill.
            label = match.group("label")
            return label[2:-1] if label.startswith("![") else label[1:-1]
        return match.group("label") + "(" + destination + (match.group("title") or "") + ")"

    # Rewrite destinations against original source locations exactly once.
    # A second pass only handles the unmatched outer link of a Markdown badge.
    text = LINK.sub(replace_link, text)
    def replace_badge(match):
        destination = match.group("target")
        # A rewritten destination already resolves within the output payload.
        output_target = (output.parent / urlsplit(destination.strip("<>")).path)
        if output_target in sources.values():
            return destination
        return target_for(destination) or destination
    return DESTINATION.sub(replace_badge, text)


def build_payload(name, root=ROOT):
    """Return {POSIX relative filename: bytes}; fail on any symlink input."""
    root = Path(root).resolve()
    directory = _safe_skill(name, root)
    selected = {}
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if any(part in EXCLUDED for part in relative.parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed in skill payloads: {path}")
        if path.is_file():
            selected[path] = relative
    for filename in ("LICENSE", "NOTICE"):
        path = root / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or unsafe required notice: {path}")
        selected[path] = Path(filename)
    for path in [root / "README.md", *(root / "docs" / name for name in DOCS)]:
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Symlink documentation or escaped path is not allowed: {path}")
        if path.is_file():
            selected[path] = Path("package-docs") / path.relative_to(root)
    sources = {source.resolve(): output for source, output in selected.items()}
    payload = {}
    for source, output in selected.items():
        content = source.read_bytes()
        if source.suffix.lower() == ".md":
            content = _rewrite_markdown(content.decode("utf-8"), source, output, sources).encode("utf-8")
        payload[output.as_posix()] = content
    return payload
