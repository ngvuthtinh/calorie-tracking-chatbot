from pydantic import BaseModel
from typing import Optional
from backend.app.schemas.common import ActivityLevel, GoalType

class UserProfile(BaseModel):
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None

class UserGoal(BaseModel):
    goal_type: GoalType
    target_weight_kg: Optional[float] = None
    daily_target_kcal: Optional[int] = None
