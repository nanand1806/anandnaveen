#!/usr/bin/env python3
"""Convert a CycloneDX JSON SBOM into a human-readable Excel workbook."""
import json
import sys
from openpyxl import Workbook


def main(src: str, out: str) -> None:
    with open(src, encoding="utf-8") as fh:
        data = json.load(fh)

    wb = Workbook()
    ws = wb.active
    ws.title = "SBOM"
    ws.append(["Name", "Version", "Type", "PURL", "Licenses"])

    for comp in data.get("components", []):
        licenses = ", ".join(
            entry.get("license", {}).get("id")
            or entry.get("license", {}).get("name")
            or ""
            for entry in comp.get("licenses", [])
        )
        ws.append([
            comp.get("name", ""),
            comp.get("version", ""),
            comp.get("type", ""),
            comp.get("purl", ""),
            licenses,
        ])

    wb.save(out)
    print(f"Wrote {out} ({ws.max_row - 1} components)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
