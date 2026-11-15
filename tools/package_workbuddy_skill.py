#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. Apache-2.0.
"""Build one WorkBuddy ZIP without changing the portable skill source.

Usage: python3 tools/package_workbuddy_skill.py mkl-uml-domain-modeler
Platform schema: https://open.workbuddy.cn/docs/skill
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

try:
    from .skill_payload import ROOT, build_payload, _rewrite_markdown
except ImportError:
    from skill_payload import ROOT, build_payload, _rewrite_markdown


def flatten_payload(payload):
    """WorkBuddy accepts only skill-root/subdirectory/file, not deeper nesting."""
    virtual = Path("/__mkl_workbuddy_payload__")
    mapping = {}
    for relative in payload:
        parts = Path(relative).parts
        target = Path(parts[0], "__".join(parts[1:])) if len(parts) > 2 else Path(relative)
        if target in mapping.values():
            raise ValueError(f"Flattened path collision: {target}")
        mapping[(virtual / relative).resolve()] = target
    flattened = {}
    for relative, content in payload.items():
        source = virtual / relative
        target = mapping[source.resolve()]
        if source.suffix.lower() == ".md":
            content = _rewrite_markdown(content.decode("utf-8"), source, target, mapping).encode("utf-8")
        flattened[target.as_posix()] = content
    return flattened


def build_icon(name, output):
    """Render the existing distinct vector mark as the required 512 px PNG."""
    vector = ROOT / "skills" / name / "assets/icon.svg"
    if not vector.is_file():
        vector = ROOT / "docs/workbuddy/icons" / f"{name}.svg"
    content = vector.read_text(encoding="utf-8").replace("currentColor", "#e9f2ff")
    graphic = ET.fromstring(content)
    graphic.attrib.update(x="76", y="76", width="360", height="360")
    content = ET.tostring(graphic, encoding="unicode")
    framed = ('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">'
              '<rect width="512" height="512" rx="92" fill="#132b46"/>'
              '<rect x="25" y="25" width="462" height="462" rx="72" fill="none" stroke="#396885" stroke-width="3"/>'
              + content + '</svg>')
    destination = Path(output) / f"{name}.png"
    subprocess.run(["rsvg-convert", "--width", "512", "--height", "512", "--output", str(destination)],
                   input=framed.encode("utf-8"), check=True)
    if destination.stat().st_size > 500 * 1024:
        raise ValueError("Icon exceeds the 500 KB form limit")
    return destination


def package(name, output=None):
    payload = flatten_payload(build_payload(name))
    catalog = json.loads((ROOT / "docs/workbuddy/skills.json").read_text(encoding="utf-8"))
    metadata = catalog[name]
    fields = ("display_name", "display_name_en", "description_zh", "description_en")
    for field in fields:
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            raise ValueError(f"Missing {field} for {name}")
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    version = metadata.get("version", version)
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Invalid platform release version: {version!r}")
    text = payload["SKILL.md"].decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    frontmatter, body = text[4:].split("\n---\n", 1)
    additions = {field: metadata[field] for field in fields}
    additions.update(version=version, author="kingle.zhuang")
    for field in ("examples_zh", "examples_en"):
        examples = metadata.get(field, [])
        if not examples or any(not isinstance(item, str) or not item.strip() for item in examples):
            raise ValueError(f"Missing examples: {field}")
        additions[field] = examples
    if re.search(r"^(?:" + "|".join(additions) + r"):", frontmatter, re.M):
        raise ValueError("Platform metadata already exists; update the adapter before overwriting it")
    lines = [f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in additions.items()]
    payload["SKILL.md"] = ("---\n" + frontmatter + "\n" + "\n".join(lines) + "\n---\n" + body).encode("utf-8")
    destination = Path(output) if output else ROOT / "dist/workbuddy"
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination / f"{name}.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative, content in sorted(payload.items()):
            info = zipfile.ZipInfo(f"{name}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    if archive_path.stat().st_size > 3 * 1024 * 1024:
        archive_path.unlink()
        raise ValueError("WorkBuddy upload exceeds the 3 MB form limit")
    result = {
        "name": name, "version": version, "pricing": "free", "archive": archive_path.name,
        "bytes": archive_path.stat().st_size, "files": len(payload),
        "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        "status": "prepared, not submitted", **additions,
    }
    (destination / f"{name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return archive_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", help="exactly one skill identifier")
    parser.add_argument("--with-icon", action="store_true", help="render the market PNG using rsvg-convert")
    args = parser.parse_args()
    try:
        archive = package(args.skill)
        print(archive)
        if args.with_icon:
            print(build_icon(args.skill, archive.parent))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
