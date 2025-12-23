from pydantic import BaseModel
from typing import List, Optional

class ExerciseItem(BaseModel):
    ex_type: str
    duration_min: Optional[int] = None
    distance_km: Optional[float] = None
    reps: Optional[int] = None
    note: Optional[str] = None
    burned_kcal: Optional[float] = None

class ExerciseEntry(BaseModel):
    entry_code: str
    items: List[ExerciseItem]
    created_at: Optional[str] = None
    total_burned_kcal: Optional[float] = None
