from pydantic import BaseModel
from typing import List, Optional
from backend.app.schemas.common import EntryDate

class DailySummary(BaseModel):
    date: EntryDate
    intake_kcal: float
    burned_kcal: float
    net_kcal: float
    target_kcal: float
    remaining_kcal: float

class WeeklySummary(BaseModel):
    days: List[DailySummary]
    total_intake: float
    total_burned: float
    avg_net: float
