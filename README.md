# PDF Merger & Word Converter

Merge multiple PDF and Word (.docx) files into a single PDF, with optional page numbering.

---

## What it does

- Upload **PDFs and/or Word documents** in any order
- Combines them into **one PDF** in the order you choose
- Optionally adds **page numbers** (e.g. `Pag. 2/40`) to every page
- Word documents are converted to PDF automatically, preserving bold, italic, headings, tables, and images

---

## Running locally

**First time setup:**

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Start the app:**

```bash
source venv/bin/activate
python app.py
```

Open **http://127.0.0.1:5050** in your browser.

**Optional — better Word formatting (images, logos):**

Install LibreOffice for the highest-quality Word-to-PDF conversion:
```bash
brew install --cask libreoffice     # macOS
sudo apt install libreoffice        # Linux/Ubuntu
```

Or install pango for image support via weasyprint:
```bash
sudo xcodebuild -license accept     # macOS only (once)
brew install pango                  # macOS
sudo apt install libpango-1.0-0 libpangoft2-1.0-0   # Linux/Ubuntu
```

---

## Deploying to Railway (recommended — full image support)

Railway supports system libraries so Word documents convert with full formatting including logos and images.

**Steps:**

1. Push your code to GitHub (this repo).
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select this repository.
4. Railway automatically detects `nixpacks.toml` and installs all required system libraries (`pango`, `cairo`, `glib`).
5. Click **Deploy**. You will receive a public URL like `yourapp.up.railway.app`.
6. To use a custom domain: go to **Settings → Domains → Add custom domain**.

No extra configuration needed — the `nixpacks.toml` and `requirements.txt` in this repo handle everything.

**What Railway installs automatically:**
- Python dependencies from `requirements.txt`
- System libraries: `pango`, `cairo`, `glib` (from `nixpacks.toml`)

---

## Deploying to Vercel (limited — no images in Word conversion)

Vercel works but cannot install system libraries, so Word documents convert without images or logos. Text, bold, italic, headings, and tables are preserved.

**Steps:**

1. Push your code to GitHub.
2. Go to [vercel.com](https://vercel.com) → **New Project** → import this repository.
3. Vercel detects `vercel.json` automatically.
4. Click **Deploy**.

**Limitation:** Word documents (.docx) that contain images or logos will convert without those images. This is a Vercel platform restriction, not a bug in the code.

---

## Deploying to a company server (VPS / Linux server)

If your company is hosting this on their own server (e.g. Ubuntu/Debian):

**Tell the server team to run:**

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libglib2.0-0

# 2. Clone the repo and set up Python environment
git clone <repo-url>
cd pdf-master2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run the app (for testing)
python app.py

# 4. For production, run with gunicorn behind nginx:
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5050 --workers 2 --timeout 120
```

**What to tell the server team:**
- This is a **Python Flask** web application.
- It requires **Python 3.10+**.
- It requires these **system libraries**: `libpango-1.0-0`, `libpangoft2-1.0-0`, `libcairo2`, `libglib2.0-0`.
- It uses the **PORT** environment variable (defaults to 5050 if not set).
- Temporary files are written to the system's `/tmp` directory during conversion and deleted automatically.
- Recommended: run with **gunicorn** behind **nginx** as a reverse proxy.
- Set timeout to at least **120 seconds** to allow Word conversion to complete.

---

## Word-to-PDF conversion quality

The app tries conversion methods in this order, using the best one available:

| Method | Quality | Requires |
|---|---|---|
| LibreOffice | Best (pixel-perfect) | `libreoffice` installed |
| docx2pdf | Great | Microsoft Word (Windows/Mac) |
| mammoth + weasyprint | Good (text + images) | `pango` system library |
| python-docx + reportlab | Basic (text only, no images) | Nothing extra |

The app always falls back gracefully — it will never crash, just use the best method available on the server.

---

## Project structure

```
app.py              – Flask web app (main entry point)
pdf_pipeline.py     – Word-to-PDF conversion and merge logic
add_page_numbers.py – Adds "Pag. n/total" headers to PDFs
pdf_controller.py   – Command-line interface
templates/          – HTML templates for the web UI
requirements.txt    – Python dependencies
nixpacks.toml       – Railway deployment config (installs system libs)
vercel.json         – Vercel deployment config
```
