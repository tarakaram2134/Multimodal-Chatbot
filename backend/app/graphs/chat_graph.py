from typing import TypedDict, Optional
import os
from PIL import Image

from ..core.vectorstore import query
from ..core.llm import generate_text, generate_vision
from ..parsers.image_store import list_images

class ChatState(TypedDict, total=False):
    session_id: str
    question: str

    has_docs: bool
    has_images: bool

    retrieved: list[dict]
    vision_answer: Optional[str]
    final_answer: str

def _route(state: ChatState) -> str:
    # This is routing based on what the session has.
    sid = state["session_id"]
    images = list_images(sid)
    state["has_images"] = len(images) > 0

    # This is assuming docs exist if retrieval returns something for the question.
    retrieved = query(sid, state["question"], top_k=1)
    state["has_docs"] = len(retrieved) > 0

    if state["has_docs"] and state["has_images"]:
        return "both"
    if state["has_images"]:
        return "vision"
    return "rag"

def _retrieve(state: ChatState) -> ChatState:
    sid = state["session_id"]
    q = state["question"]
    state["retrieved"] = query(sid, q, top_k=5)
    return state

def _vision(state: ChatState) -> ChatState:
    sid = state["session_id"]
    q = state["question"]
    images = list_images(sid)
    if not images:
        state["vision_answer"] = None
        return state

    # This is using the latest uploaded image for the session.
    latest = sorted(images, key=lambda p: os.path.getmtime(p))[-1]

    with open(latest, "rb") as f:
        img_bytes = f.read()

    mime = "image/png"
    lower = latest.lower()
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        mime = "image/jpeg"
    elif lower.endswith(".webp"):
        mime = "image/webp"

    prompt = (
        "You are analyzing an uploaded image for a user.\n"
        "Answer the question using only what is visible in the image.\n"
        "If the image does not contain enough information, say what is missing.\n\n"
        f"Question: {q}"
    )
    state["vision_answer"] = generate_vision(prompt, img_bytes, mime)
    return state

def _final(state: ChatState) -> ChatState:
    q = state["question"]
    retrieved = state.get("retrieved", [])
    vision_answer = state.get("vision_answer")

    context_blocks = []
    citations = []

    for r in retrieved:
        meta = r.get("metadata", {})
        snippet = r["text"]
        source = meta.get("source", "uploaded")
        page = meta.get("page")
        citations.append({"source": source, "page": page, "snippet": snippet[:220]})
        context_blocks.append(f"[Source: {source} | Page: {page}]\n{snippet}")

    context_text = "\n\n".join(context_blocks).strip()

    if context_text and vision_answer:
        system = (
            "You are a helpful assistant. Use the provided document context and the image analysis.\n"
            "If they conflict, say so.\n"
            "When using document context, keep it grounded.\n"
        )
        prompt = (
            f"{system}\n"
            f"Question: {q}\n\n"
            f"Document context:\n{context_text}\n\n"
            f"Image analysis:\n{vision_answer}\n\n"
            "Write the final answer."
        )
    elif vision_answer:
        system = (
            "You are a helpful assistant. Answer using ONLY the provided image analysis.\n"
            "If the image analysis is insufficient, say so.\n"
        )
        prompt = (
            f"{system}\n"
            f"Question: {q}\n\n"
            f"Image analysis:\n{vision_answer}\n\n"
            "Write the answer."
        )   
    elif context_text:
        system = (
            "You are a helpful assistant. Answer using ONLY the provided document context.\n"
            "If the context is insufficient, say so.\n"
        )
        prompt = (
            f"{system}\n"
            f"Question: {q}\n\n"
            f"Context:\n{context_text}\n\n"
            "Write the answer."
        )
    else:
        system = (
            "You are a helpful assistant.\n"
            "Answer the question directly. If you need the user to upload a PDF/text/image, say so.\n"
        )
        prompt = f"{system}\nQuestion: {q}\n"

    answer = generate_text(prompt)
    state["final_answer"] = answer
    state["citations"] = citations
    return state

def run_graph(session_id: str, question: str) -> dict:
    # This is running a small routing pipeline without overcomplicating the graph.
    state: ChatState = {"session_id": session_id, "question": question}

    route = _route(state)

    if route in ("rag", "both"):
        state = _retrieve(state)
    if route in ("vision", "both"):
        state = _vision(state)

    state = _final(state)

    return {
        "answer": state["final_answer"],
        "citations": state.get("citations", []),
        "used_docs": bool(state.get("has_docs")),
        "used_image": bool(state.get("has_images")),
    }
