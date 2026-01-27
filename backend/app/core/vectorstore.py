import os
import uuid
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from .config import CHROMA_DIR

_EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_embedder = SentenceTransformer(_EMBED_MODEL_NAME)

def _get_client() -> chromadb.Client:
    os.makedirs(CHROMA_DIR, exist_ok=True)
    return chromadb.PersistentClient(
        path=CHROMA_DIR,
        settings=Settings(anonymized_telemetry=False),
    )

def get_collection():
    client = _get_client()
    return client.get_or_create_collection(name="docs")

def upsert_chunks(session_id: str, chunks: list[dict]) -> int:
    # chunks items: {"text": ..., "metadata": {...}}
    if not chunks:
        return 0

    collection = get_collection()

    texts = [c["text"] for c in chunks]
    metas = []
    ids = []

    # This is embedding once per chunk and storing session-aware metadata.
    vectors = _embedder.encode(texts, normalize_embeddings=True).tolist()

    for c in chunks:
        meta = dict(c.get("metadata", {}))
        meta["session_id"] = session_id
        metas.append(meta)
        ids.append(str(uuid.uuid4()))

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metas,
    )
    return len(texts)

def query(session_id: str, question: str, top_k: int = 5) -> list[dict]:
    collection = get_collection()

    q_vec = _embedder.encode([question], normalize_embeddings=True).tolist()[0]

    # This is filtering by session_id so users never see each other's docs.
    res = collection.query(
        query_embeddings=[q_vec],
        n_results=top_k,
        where={"session_id": session_id},
        include=["documents", "metadatas", "distances"],
    )

    results = []
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    for doc, meta, dist in zip(docs, metas, dists):
        results.append({
            "text": doc,
            "metadata": meta or {},
            "distance": float(dist),
        })
    return results
