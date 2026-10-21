#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Maintain stable, scoped artifact identifiers without renumbering existing work.

A key is an artifact identity, not its current title or display position. Missing
keys are retained. Retirement must be explicit and never frees an identifier.
"""
import argparse
import copy
import json
import re
from pathlib import Path


def reconcile(registry, prefix, keys, retire=(), namespace="project"):
    if not re.fullmatch(r"[A-Z][A-Z0-9]*", prefix):
        raise ValueError("prefix must use uppercase letters and digits")
    if not namespace.strip():
        raise ValueError("namespace must not be blank")
    out = copy.deepcopy(registry)
    if out.get("version") != 1 or not isinstance(out.get("namespaces"), dict):
        raise ValueError("expected registry version 1 and namespaces object")
    group = out["namespaces"].setdefault(namespace, {}).setdefault(
        prefix, {"high_water": 0, "assignments": {}})
    assignments = group.get("assignments")
    high = group.get("high_water")
    if not isinstance(assignments, dict) or type(high) is not int or high < 0:
        raise ValueError("invalid assignments or high_water")
    seen, maximum = set(), 0
    for key, entry in assignments.items():
        if not isinstance(key, str) or not key.strip() or not isinstance(entry, dict):
            raise ValueError("invalid artifact identity")
        match = re.fullmatch(re.escape(prefix) + r"-(\d{2,})", entry.get("id", ""))
        if not match or entry.get("state") not in {"active", "retired"}:
            raise ValueError("invalid identifier or state")
        number = int(match.group(1))
        if number < 1 or number in seen:
            raise ValueError("duplicate or nonpositive identifier")
        seen.add(number)
        maximum = max(maximum, number)
    if high < maximum:
        raise ValueError("high_water is below an existing identifier")
    keys, retire = list(keys), list(retire)
    if any(not isinstance(k, str) or not k.strip() for k in keys + retire):
        raise ValueError("artifact keys must not be blank")
    if set(keys) & set(retire):
        raise ValueError("cannot request and retire the same artifact")
    for key in retire:
        if key not in assignments:
            raise ValueError("cannot retire an unknown artifact: " + key)
        assignments[key]["state"] = "retired"
    for key in keys:
        if key in assignments:
            if assignments[key]["state"] == "retired":
                raise ValueError("retired artifact cannot be reused: " + key)
            continue
        high += 1
        assignments[key] = {"id": f"{prefix}-{high:02d}", "state": "active"}
    group["high_water"] = high
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, help="existing JSON registry; omitted for a new registry")
    parser.add_argument("--namespace", default="project", help="project or parent CU ID for local flow IDs")
    parser.add_argument("--prefix", required=True, help="CU, DR, DS, MC, CP, FA, FE, or another established prefix")
    parser.add_argument("--key", action="append", default=[], help="stable artifact identity; repeatable")
    parser.add_argument("--retire", action="append", default=[], help="explicitly retire an identity; repeatable")
    args = parser.parse_args()
    try:
        current = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry else {"version": 1, "namespaces": {}}
        updated = reconcile(current, args.prefix, args.key, args.retire, args.namespace)
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        parser.error(str(exc))
    print(json.dumps(updated, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
