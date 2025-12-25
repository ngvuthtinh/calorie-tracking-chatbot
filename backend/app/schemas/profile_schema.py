from pydantic import BaseModel
from typing import Optional, Literal

class ProfileUpdateRequest(BaseModel):
    user_id: int # Required mainly for identity if not using JWT yet
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[Literal["low", "moderate", "high"]] = None
    goal_type: Optional[Literal["lose", "maintain", "gain"]] = None
    target_weight_kg: Optional[float] = None

class ProfileResponse(BaseModel):
    success: bool
    message: str
    profile: Optional[dict] = None  # Full profile object
    goal: Optional[dict] = None     # Full goal object
    health_metrics: Optional[dict] = None # Calculated (BMI, TDEE)
