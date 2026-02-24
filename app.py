"""
Web app: (1) Add page numbers to a PDF. (2) Merge PDF & Word and optionally add page numbers.
"""

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
    # POST: merge files
    if "files[]" in request.files:
        files = request.files.getlist("files[]")
    else:
        files = request.files.getlist("files") if "files" in request.files else []
    files = [f for f in files if f and f.filename]
    if not files:
        return "No files uploaded", 400
    enumerate_pages = request.form.get("enumerate", "false").lower() in ("1", "true", "yes")
    output_name = (request.form.get("output_name", "").strip() or "merged_output")
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        paths = []
        for f in files:
            path = tmp / (f.filename or "file")
            path.write_bytes(f.read())
            paths.append(path)
        try:
            out_path = tmp / output_name
            build_merged_pdf(paths, out_path, enumerate=enumerate_pages, temp_dir=tmp)
            return send_file(
                out_path,
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
