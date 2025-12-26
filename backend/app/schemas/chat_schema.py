from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class ChatRequest(BaseModel):
    """
    Request schema for the chat endpoint.
    """
    user_id: int = Field(..., description="Unique identifier for the user")
    entry_date: Optional[Any] = Field(None, description="Date for the entry in YYYY-MM-DD format. Defaults to today if not provided.")
    text: str = Field(..., min_length=1, description="User's natural language input")
    
    @validator('entry_date', pre=True, always=True)
    def validate_and_default_date(cls, v):
        """Validate that entry_date is in YYYY-MM-DD format, or default to today."""
        if v is None or v == "":
            return datetime.now().date()
        if isinstance(v, date):
            return v
        if isinstance(v, datetime):
            return v.date()
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('entry_date must be in YYYY-MM-DD format (YYYY-MM-DD)')

    @validator('text')
    def validate_text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Please provide a message to process.')
        return v


class ChatActionResponse(BaseModel):
    """
    Response schema for the chat endpoint.
    """
    success: bool = Field(..., description="Whether the operation succeeded")
    message: str = Field(..., description="User-friendly message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Structured data from the operation")
    frame: Optional[Dict[str, Any]] = Field(None, description="Parsed semantic frame (for debugging)")
