from pydantic import BaseModel
from typing import List, Optional
from backend.app.schemas.common import MealType, ActionType

class FoodItem(BaseModel):
    name: str
    qty: float
    unit: str
    note: Optional[str] = None
    kcal: Optional[float] = None

class FoodEntry(BaseModel):
    entry_code: str
    meal: Optional[MealType] = None
    action: Optional[ActionType] = None
    items: List[FoodItem]
    created_at: Optional[str] = None  # ISO format string or datetime
    intake_kcal: Optional[float] = None
