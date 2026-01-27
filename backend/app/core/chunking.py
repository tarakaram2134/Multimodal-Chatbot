from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    metadata: dict

def simple_chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[Chunk]:
    # This is keeping chunking predictable and debuggable.
    clean = " ".join(text.split())
    if not clean:
        return []

    chunks: list[Chunk] = []
    start = 0
    while start < len(clean):
        end = min(len(clean), start + chunk_size)
        chunk_text = clean[start:end].strip()
        if chunk_text:
            chunks.append(Chunk(text=chunk_text, metadata={}))
        if end == len(clean):
            break
        start = max(0, end - overlap)
    return chunks
