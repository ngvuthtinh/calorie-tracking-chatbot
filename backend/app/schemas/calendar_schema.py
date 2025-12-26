from pydantic import BaseModel
from typing import List, Optional

class LogEntry(BaseModel):
    id: int
    type: str  # 'food', 'exercise'
    name: str # e.g. "Chicken Breast"
    calories: float
    time: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None

class DaySummary(BaseModel):
    intake_kcal: float
    burned_kcal: float
    net_kcal: float
    target_kcal: float
    remaining_kcal: float

class CoachAdvice(BaseModel):
    status: str
    message: str

class DayViewResponse(BaseModel):
    date: str
    food_entries: List[LogEntry]
    exercise_entries: List[LogEntry]
    summary: DaySummary
    coach_advice: Optional[CoachAdvice] = None

class MonthDayStatus(BaseModel):
    date: str
    status: str
    net_kcal: float

class MonthViewResponse(BaseModel):
    month: str
    days: List[MonthDayStatus]

class OverviewStats(BaseModel):
    total_days_logged: int
    current_streak: int
    weight_start: float
    weight_current: float
    start_date: str
