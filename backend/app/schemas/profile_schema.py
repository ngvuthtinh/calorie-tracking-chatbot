from pydantic import BaseModel
from typing import Optional, Literal

class ProfileUpdateRequest(BaseModel):
    user_id: int
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    activity_level: Optional[Literal["sedentary", "light", "moderate", "active", "very_active"]] = None
    goal_type: Optional[Literal["lose_weight", "maintain_weight", "gain_weight"]] = None
    target_weight_kg: Optional[float] = None

class ProfileResponse(BaseModel):
    success: bool
    message: str
    profile: Optional[dict] = None  # e.g. { weight_kg, height_cm, age, gender, activity_level }
    goal: Optional[dict] = None     # e.g. { type, daily_target_kcal, target_weight_kg }
    health_metrics: Optional[dict] = None # e.g. { bmi, tdee, bmr }
