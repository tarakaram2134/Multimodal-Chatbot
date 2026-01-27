from pydantic import BaseModel
from typing import Any

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[dict[str, Any]]
    used_docs: bool
    used_image: bool
