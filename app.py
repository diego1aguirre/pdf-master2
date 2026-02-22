"""
Web app: upload a PDF, get back the same PDF with "Pag. n/total" on each page.
"""

import tempfile
from pathlib import Path

from flask import Flask, render_template, request, send_file

from add_page_numbers import add_numbers_to_pdf

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


PORT = 5050

if __name__ == "__main__":
    print("\n  PDF Page Numbers – open in your browser:\n")
    print(f"    http://127.0.0.1:{PORT}")
    print("\n  (Stop the server with Ctrl+C)\n")
    app.run(host="0.0.0.0", debug=True, port=PORT)
