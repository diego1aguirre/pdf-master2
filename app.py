"""
Web app: (1) Add page numbers to a PDF. (2) Merge PDF & Word and optionally add page numbers.
"""

import io
import tempfile
from pathlib import Path

from flask import Flask, render_template, request, send_file

from add_page_numbers import add_numbers_to_pdf
from pdf_pipeline import build_merged_pdf

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    if "pdf" not in request.files:
        return "No file uploaded", 400
    file = request.files["pdf"]
    if not file or file.filename == "":
        return "No file selected", 400
    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed", 400

    with tempfile.TemporaryDirectory() as tmp:
        input_path = Path(tmp) / "input.pdf"
        output_path = Path(tmp) / "output_numbered.pdf"
        file.save(input_path)
        add_numbers_to_pdf(input_path, output_path)
        base = Path(file.filename).stem
        download_name = f"{base}_iloveVerum.pdf"
        return send_file(
            output_path,
            as_attachment=True,
            download_name=download_name,
            mimetype="application/pdf",
        )


@app.route("/merge", methods=["GET", "POST"])
def merge():
    if request.method == "GET":
        return render_template("merge.html")
    # POST: merge files — support "files", "files[]", or any multi-part file field
    files = request.files.getlist("files") or request.files.getlist("files[]")
    if not files:
        files = [v for v in request.files.values() if v and getattr(v, "filename", None)]
    files = [f for f in files if f and getattr(f, "filename", None)]
    if not files:
        return "No files uploaded. Select one or more PDF or DOCX files.", 400
    enumerate_pages = request.form.get("enumerate", "false").lower() in ("1", "true", "yes")
    output_name = (request.form.get("output_name", "").strip() or "merged_output")
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        paths = []
        name_count = {}
        for f in files:
            base = f.filename or "file"
            if base not in name_count:
                name_count[base] = 0
            name_count[base] += 1
            if name_count[base] > 1:
                stem, ext = base.rsplit(".", 1) if "." in base else (base, "")
                base = f"{stem}_{name_count[base]}.{ext}" if ext else f"{stem}_{name_count[base]}"
            path = tmp / base
            path.write_bytes(f.read())
            paths.append(path)
        try:
            out_path = tmp / output_name
            build_merged_pdf(paths, out_path, enumerate=enumerate_pages, temp_dir=tmp)
            pdf_bytes = out_path.read_bytes()
            return send_file(
                io.BytesIO(pdf_bytes),
                as_attachment=True,
                download_name=output_name,
                mimetype="application/pdf",
            )
        except Exception as e:
            return str(e), 500


PORT = 5050

if __name__ == "__main__":
    print("\n  PDF Page Numbers – open in your browser:\n")
    print(f"    http://127.0.0.1:{PORT}")
    print("\n  (Stop the server with Ctrl+C)\n")
    app.run(host="0.0.0.0", debug=True, port=PORT)
