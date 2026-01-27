import fitz  # PyMuPDF

def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    # This is extracting per-page text so citations can include page numbers.
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text") or ""
        pages.append({"page": i + 1, "text": text})
    return pages
