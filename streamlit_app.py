"""
Streamlit UI: upload/select files in order, toggle Enumerate, run merge pipeline.
"""

import tempfile
from pathlib import Path

import streamlit as st

from pdf_pipeline import build_merged_pdf

st.set_page_config(page_title="PDF Merger", page_icon="📄", layout="centered")

st.title("Merge PDF & Word documents")
st.caption("Upload PDFs and/or DOCX files. Order is preserved. Optionally add page numbers.")

# File upload (multiple)
uploaded = st.file_uploader(
    "Choose files (order = merge order)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

if not uploaded:
    st.info("Upload one or more PDF or DOCX files to get started.")
    st.stop()

# Show order and allow reordering via position
st.subheader("Order of documents")
names = [f.name for f in uploaded]
for i, name in enumerate(names):
    st.caption(f"{i + 1}. {name}")

# Enumerate toggle
enumerate_pages = st.checkbox("Add page numbers (Pag. n/total) in header", value=True)

# Output filename
output_name = st.text_input("Output filename", value="merged_output.pdf")
if not output_name.strip().endswith(".pdf"):
    output_name = (output_name.strip() or "merged_output") + ".pdf"

if st.button("Merge and download"):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        paths = []
        for f in uploaded:
            p = tmp / f.name
            p.write_bytes(f.getvalue())
            paths.append(p)
        out_path = tmp / output_name.strip()
        try:
            build_merged_pdf(paths, out_path, enumerate=enumerate_pages, temp_dir=tmp)
            if out_path.exists():
                st.session_state["merged_pdf_bytes"] = out_path.read_bytes()
                st.session_state["merged_pdf_name"] = output_name.strip()
                st.rerun()
        except Exception as e:
            st.error(str(e))

if st.session_state.get("merged_pdf_bytes"):
    st.download_button(
        label="Download merged PDF",
        data=st.session_state["merged_pdf_bytes"],
        file_name=st.session_state.get("merged_pdf_name", "merged_output.pdf"),
        mime="application/pdf",
    )
