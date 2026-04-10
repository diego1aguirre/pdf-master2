# PDF Merger & Word Converter

A web application for merging PDF and Word (.docx) files into a single PDF, with optional page numbering.

---

## Features

- Merge any combination of **PDF and Word documents** into one PDF
- Preserves the **order you choose** for the final document
- Optional **page numbering** on every page (`Pag. 1/10` style)
- Word documents are converted automatically, preserving bold, italic, headings, tables, and images

---

## Requirements

- Python 3.10+
- pip

---

## Local Development

```bash
# Clone the repository
git clone https://github.com/diego1aguirre/pdf-master2.git
cd pdf-master2

# Create a virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start the development server
python app.py
```

Open **http://127.0.0.1:5050** in your browser.

### Improving Word conversion quality (optional)

By default the app converts Word documents using pure Python libraries. For better output — including logos and images — install one of the following:

**LibreOffice** (best quality):
```bash
brew install --cask libreoffice     # macOS
sudo apt install libreoffice        # Ubuntu/Debian
```

**Pango** (enables image rendering via weasyprint):
```bash
# macOS
sudo xcodebuild -license accept
brew install pango

# Ubuntu/Debian
sudo apt install libpango-1.0-0 libpangoft2-1.0-0
```

---

## Deployment

### Railway (recommended)

Railway supports system-level libraries, so Word documents convert with full formatting including logos and images.

1. Push the repository to GitHub.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select this repository — Railway detects `nixpacks.toml` automatically and installs all required dependencies.
4. Click **Deploy**.

A public URL is generated automatically. Custom domains can be configured under **Settings → Domains**.

### Vercel

Vercel does not support system-level libraries, so Word documents convert without embedded images or logos. Text, headings, bold, italic, and tables are preserved.

1. Push the repository to GitHub.
2. Go to [vercel.com](https://vercel.com) → **New Project** → import the repository.
3. Vercel detects `vercel.json` automatically.
4. Click **Deploy**.

### Linux Server (VPS)

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libglib2.0-0

# Clone and set up
git clone https://github.com/diego1aguirre/pdf-master2.git
cd pdf-master2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with gunicorn (production)
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5050 --workers 2 --timeout 120
```

The app reads the `PORT` environment variable and defaults to `5050` if not set.

---

## Word-to-PDF Conversion

The app tries the following methods in order, using the best one available on the host:

| Method | Quality | Requirement |
|---|---|---|
| LibreOffice | Best | `libreoffice` installed |
| docx2pdf | Great | Microsoft Word (Windows/Mac) |
| mammoth + weasyprint | Good — includes images | `pango` system library |
| python-docx + reportlab | Basic — text only | None |

---

## Project Structure

```
app.py              – Flask application entry point
pdf_pipeline.py     – Word-to-PDF conversion and merge logic
add_page_numbers.py – Page numbering logic
pdf_controller.py   – Command-line interface
templates/          – HTML templates
requirements.txt    – Python dependencies
nixpacks.toml       – Railway build configuration
vercel.json         – Vercel build configuration
```
