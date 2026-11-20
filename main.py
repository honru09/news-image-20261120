"""make.fun competition entrypoint — news-image-20261120.

Copies the pre-rendered 20 November 2026 world news infographic
(entry.png, 1024x1024, sha256 5ec4868950a207c275b29ebae3c2a27e00ff166015712d09c339389b9eef73dd)
to the target harness output directory (MAKEFUN_OUTPUT_DIR or /output).
Uses Python standard library only; no external dependencies required.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

DEFAULT_OUTPUT_DIR = "/output"
IMAGE_FILENAME = "entry.png"


def resolve_output_dir() -> Path:
    """Determine target output directory from environment or fallback."""
    raw_path = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    path = Path(raw_path).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def copy_entry_image(destination_dir: Path) -> Path:
    """Copy bundled entry.png to the target directory with size verification."""
    source_path = Path(__file__).parent.resolve() / IMAGE_FILENAME
    if not source_path.is_file():
        raise FileNotFoundError(f"Missing required source infographic: {source_path}")

    destination_path = destination_dir / IMAGE_FILENAME
    shutil.copy2(source_path, destination_path)

    # Sanity check: confirm the file was written and is non-empty
    if not destination_path.is_file() or destination_path.stat().st_size == 0:
        raise IOError(f"Output file verification failed: {destination_path}")

    return destination_path


def main() -> int:
    try:
        out_dir = resolve_output_dir()
        dest = copy_entry_image(out_dir)
        print(f"[makefun] entry.png delivered -> {dest} ({dest.stat().st_size} bytes)")
        return 0
    except Exception as err:
        sys.stderr.write(f"[makefun:error] Failed to copy entry image: {err}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
