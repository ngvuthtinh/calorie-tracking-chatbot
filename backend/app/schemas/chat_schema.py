from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    user_id: int
    entry_date: str  # YYYY-MM-DD
    text: str

class ChatActionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None
    frame: Optional[Dict[str, Any]] = None
