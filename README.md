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

## Merge PDF & Word (main controller)

Merge a list of PDF and/or DOCX files into one PDF in order, with an option to add page numbers.

**Pipeline:** DOCX → PDF (via docx2pdf or LibreOffice), then merge with pypdf, then optionally run the same “Pag. n/total” header as above.

### CLI

```bash
# Activate venv first, then:
python pdf_controller.py file1.pdf doc2.docx file3.pdf -o merged.pdf
python pdf_controller.py file1.pdf file2.pdf -o merged.pdf -e   # with page numbers
```

- **Files:** Pass paths in the order you want them in the final PDF. Supports `.pdf` and `.docx`.
- **-o, --output:** Output path (default: `merged_output.pdf`).
- **-e, --enumerate:** Add “Pag. n/total” to each page.

### Streamlit UI

Upload files in order, toggle “Add page numbers”, then merge and download:

```bash
streamlit run streamlit_app.py
```

### DOCX conversion

- **Windows:** `docx2pdf` uses Microsoft Word (must be installed).
- **Mac:** `docx2pdf` uses Word (if installed) or you can use LibreOffice. Fallback: install LibreOffice and ensure `soffice` is on PATH (e.g. `brew install --cask libreoffice`).
- **Linux:** LibreOffice headless (`soffice`) is used when available.
