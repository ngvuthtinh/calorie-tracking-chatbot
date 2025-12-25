from fastapi import APIRouter, HTTPException
from backend.app.schemas.chat_schema import ChatRequest, ChatActionResponse

router = APIRouter()

# --- Endpoint ---
@router.post("/", response_model=ChatActionResponse)
async def chat_endpoint(request: ChatRequest) -> ChatActionResponse:
    """
    Main chatbot endpoint.
    Strict Contract:
    - Input: user_id, entry_date (required), text.
    - Output: success, message, data, actions.
    """
    # Placeholder for logic
    return ChatActionResponse(
        success=True,
        message=f"Received: {request.text}",
        data={"processed": True},
        actions=[]
    )
