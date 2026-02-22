#!/usr/bin/env python3
"""
Add page counter "Pag. {current}/{total}" to every page of PDFs in a folder.
Saves modified files with a "_numbered" suffix.
"""

import io
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

# ---------- HEADER: page number location & size ----------
# Placed in the header: top-right, 0.25 in from top, 1 in from right (clear of body margin).
FONT_SIZE = 18
HEADER_TOP_PT = 35      # 0.25 in from top of page to baseline
HEADER_RIGHT_MARGIN_PT = 20   # 1 in from right edge (right edge of text sits here)
# ------------------------------------------------------------------

# Prefer Arial when available (e.g. macOS); otherwise use PDF built-in Helvetica.
def _get_font_name() -> str:
    if sys.platform == "darwin":
        arial_paths = [
            Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
            Path("/Library/Fonts/Arial.ttf"),
        ]
        for path in arial_paths:
            if path.exists():
                try:
                    from reportlab.pdfbase import pdfmetrics
                    from reportlab.pdfbase.ttfonts import TTFont
                    pdfmetrics.registerFont(TTFont("Arial", str(path)))
                    return "Arial"
                except Exception:
                    break
    return "Helvetica"

FONT_NAME = _get_font_name()


def create_page_number_overlay(width_pt: float, height_pt: float, current: int, total: int) -> bytes:
    """Create a single-page PDF overlay with 'Pag. current/total' in the header (top-right)."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(width_pt, height_pt))

    # Header: top-right — change HEADER_TOP_PT / HEADER_RIGHT_MARGIN_PT at top of file
    baseline_y = height_pt - HEADER_TOP_PT
    x_right = width_pt - HEADER_RIGHT_MARGIN_PT

    text = f"Pag. {current}/{total}"
    c.setFont(FONT_NAME, FONT_SIZE)
    c.drawRightString(x_right, baseline_y, text)

    c.save()
    buffer.seek(0)
    return buffer.read()


def add_numbers_to_pdf(input_path: Path, output_path: Path) -> None:
    """Add 'Pag. n/total' to each page and save to output_path."""
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    writer = PdfWriter()

    for page_num in range(total_pages):
        page = reader.pages[page_num]
        mediabox = page.mediabox
        width_pt = float(mediabox.width)
        height_pt = float(mediabox.height)

        overlay_pdf_bytes = create_page_number_overlay(
            width_pt, height_pt, page_num + 1, total_pages
        )
        overlay_reader = PdfReader(io.BytesIO(overlay_pdf_bytes))
        overlay_page = overlay_reader.pages[0]

        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)


def process_folder(folder: Path) -> None:
    """Find all PDFs in folder (non-recursive) and add page numbers with _numbered suffix."""
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    pdf_files = sorted(folder.glob("*.pdf"))
    # Skip already numbered files to avoid double numbering
    pdf_files = [f for f in pdf_files if not f.stem.endswith("_numbered")]

    for pdf_path in pdf_files:
        out_name = f"{pdf_path.stem}_numbered.pdf"
        output_path = pdf_path.parent / out_name
        add_numbers_to_pdf(pdf_path, output_path)
        print(f"Created: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        folder = Path.cwd()
        print(f"No folder given; using current directory: {folder}")
    else:
        folder = Path(sys.argv[1])

    process_folder(folder)
