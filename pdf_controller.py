#!/usr/bin/env python3
"""
Main controller: merge PDFs and DOCX (with optional page numbering).
Use as CLI or import run_pipeline for other UIs.
"""

import argparse
import sys
from pathlib import Path

from pdf_pipeline import build_merged_pdf


def run_pipeline(
    file_paths: list[str] | list[Path],
    output_path: str | Path,
    enumerate: bool = False,
) -> Path:
    """
    Run the full pipeline: convert DOCX → PDF, merge in order, optionally add numbers.
    """
    paths = [Path(p).resolve() for p in file_paths]
    out = Path(output_path).resolve()
    return build_merged_pdf(paths, out, enumerate=enumerate)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge PDF and DOCX files into one PDF (order preserved). Optionally add page numbers."
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Paths to .pdf and/or .docx files in the order they should appear",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("merged_output.pdf"),
        help="Output PDF path (default: merged_output.pdf)",
    )
    parser.add_argument(
        "-e", "--enumerate",
        action="store_true",
        help="Add 'Pag. n/total' header to each page",
    )
    args = parser.parse_args()

    try:
        result = run_pipeline(args.files, args.output, enumerate=args.enumerate)
        print(f"Created: {result}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: file not found: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
