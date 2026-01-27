from fastapi import APIRouter
from ..schemas.api_models import ChatRequest, ChatResponse
from ..graphs.chat_graph import run_graph

router = APIRouter()

from fastapi.responses import JSONResponse
from google.genai.errors import ClientError

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        result = run_graph(req.session_id, req.message)
        return result
    except ClientError as e:
        # Handle 429 or other API errors
        return JSONResponse(
            status_code=429 if "429" in str(e) else 400,
            content={"error": f"Google GenAI API Error: {str(e)}"}
        )
    except Exception as e:
        # Generic fallback
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal Server Error: {str(e)}"}
        )
