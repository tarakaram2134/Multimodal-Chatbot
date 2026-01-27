from fastapi import APIRouter, UploadFile, File, Form
from ..parsers.pdf_parser import extract_pdf_pages
from ..parsers.text_parser import parse_text_bytes
from ..parsers.image_store import save_image
from ..core.chunking import simple_chunk_text
from ..core.vectorstore import upsert_chunks

router = APIRouter()

@router.post("/ingest")
async def ingest_files(
    session_id: str = Form(...),
    files: list[UploadFile] = File(...),
):
    total_added = 0

    for f in files:
        raw = await f.read()
        name = f.filename or "uploaded"
        lower = name.lower()

        if lower.endswith(".pdf"):
            pages = extract_pdf_pages(raw)
            chunks = []
            for p in pages:
                page_num = p["page"]
                page_text = p["text"]
                for c in simple_chunk_text(page_text):
                    meta = {"source": name, "page": page_num, "type": "pdf"}
                    chunks.append({"text": c.text, "metadata": meta})
            total_added += upsert_chunks(session_id, chunks)

        elif lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
            # This is storing images per session so chat can use vision later.
            save_image(session_id, name, raw)

        else:
            text = parse_text_bytes(raw)
            chunks = []
            for c in simple_chunk_text(text):
                meta = {"source": name, "page": None, "type": "text"}
                chunks.append({"text": c.text, "metadata": meta})
            total_added += upsert_chunks(session_id, chunks)

    return {"status": "ok", "documents_added": total_added}
