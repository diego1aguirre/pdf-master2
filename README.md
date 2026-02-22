# pdf-master2
Merge multiple PDF files and add dynamic page numbering.

## Add page numbers to PDFs

The script `add_page_numbers.py` adds a page counter **"Pag. {current}/{total}"** (e.g. `Pag. 2/40`) in the top-right corner of every page, then saves files with a `_numbered` suffix.

**Requirements:** Python 3, `pypdf`, `reportlab` (see `requirements.txt`).

**Usage:**

```bash
pip install -r requirements.txt
python add_page_numbers.py                    # process current directory
python add_page_numbers.py /path/to/folder    # process a specific folder
```

**Details:**
- Format: `Pag. {current}/{total}` (e.g. Pag. 2/40)
- Font: Arial when available (macOS), otherwise Helvetica; size 18pt
- Position: 0.25 in (18 pt) from top edge, right-aligned with 1 in (72 pt) from the right edge
- Output: `original_name_numbered.pdf` (files already ending in `_numbered` are skipped)
