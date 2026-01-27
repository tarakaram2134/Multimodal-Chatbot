import os
from ..core.config import UPLOADS_DIR

def ensure_session_dir(session_id: str) -> str:
    # This is creating a per-session folder for uploads.
    session_dir = os.path.join(UPLOADS_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def save_image(session_id: str, filename: str, data: bytes) -> str:
    session_dir = ensure_session_dir(session_id)
    safe_name = filename.replace("/", "_").replace("\\", "_")
    path = os.path.join(session_dir, safe_name)
    with open(path, "wb") as f:
        f.write(data)
    return path

def list_images(session_id: str) -> list[str]:
    session_dir = os.path.join(UPLOADS_DIR, session_id)
    if not os.path.isdir(session_dir):
        return []
    return [
        os.path.join(session_dir, f)
        for f in os.listdir(session_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ]
