from google import genai
from google.genai import types
from .config import GEMINI_API_KEY

_TEXT_MODEL = "gemini-2.5-flash-lite"
_VISION_MODEL = "gemini-2.5-flash-lite"

_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_text(prompt: str) -> str:
    response = _client.models.generate_content(
        model=_TEXT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1024,
        ),
    )
    return (response.text or "").strip()

def generate_vision(prompt: str, image_bytes: bytes, mime_type: str) -> str:
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    response = _client.models.generate_content(
        model=_VISION_MODEL,
        contents=[prompt, image_part],
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1024,
        ),
    )
    return (response.text or "").strip()
