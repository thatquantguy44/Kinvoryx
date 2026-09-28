#!/usr/bin/env python3
"""Run metadata-only checks for Home Sweet Home zero-dollar source candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from kinvoryx.housing_sources import run_source_checks  # noqa: E402


def load_yaml_config(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("PyYAML is required to read the source YAML config") from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping at the top of {path}")
    return data


def status_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in results:
        status = str(result.get("status", "unknown"))
        counts[status] = counts.get(status, 0) + 1
    return dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run read-only, metadata-only source checks for Home Sweet Home.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "config" / "home_sweet_home.sources.local.yaml",
        help="Path to ignored local source YAML.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON metadata output path. Raw API payloads are never stored.",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print metadata JSON to stdout. This does not include configured secrets.",
    )
    args = parser.parse_args()

    config = load_yaml_config(args.config)
    report = run_source_checks(config)

    output_path: Path | None = args.output
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    counts = status_counts(report["results"])
    print(
        "Home Sweet Home source check complete: "
        + ", ".join(f"{status}={count}" for status, count in counts.items())
    )
    if output_path is not None:
        print(f"metadata_report={output_path}")
    if args.print_json:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
