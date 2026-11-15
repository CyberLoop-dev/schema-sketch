#!/usr/bin/env python3
"""Print a compact summary of a JSON Schema document."""

import argparse
import json
from pathlib import Path


def describe(schema: dict, indent: int = 0) -> list[str]:
    pad = " " * indent
    title = schema.get("title", "(untitled)")
    kind = schema.get("type", "unspecified")
    lines = [f"{pad}{title}: {kind}"]
    required = set(schema.get("required", []))
    for name, spec in schema.get("properties", {}).items():
        marker = "required" if name in required else "optional"
        lines.append(f"{pad}  - {name}: {spec.get('type', 'unspecified')} ({marker})")
        if spec.get("type") == "object":
            lines.extend(describe(spec, indent + 4))
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", type=Path)
    args = parser.parse_args()
    data = json.loads(args.schema.read_text(encoding="utf-8"))
    print("\n".join(describe(data)))


if __name__ == "__main__":
    main()
