import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Put it in .env")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
