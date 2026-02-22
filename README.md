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

## Web app (test in the browser)

Upload a PDF and download the numbered version.

**First time (create a virtual environment and install dependencies):**

```bash
cd pdf-master2
python3 -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Every time you want to run the app:**

1. Open a terminal in the project folder.
2. Activate the venv and start the server:
   ```bash
   source venv/bin/activate
   python app.py
   ```
3. In your browser, open the URL shown (e.g. **http://127.0.0.1:5050**).
4. Choose a PDF and click “Add page numbers” to download the numbered file.

(Port 5050 is used because 5000 is often taken by macOS AirPlay.)
