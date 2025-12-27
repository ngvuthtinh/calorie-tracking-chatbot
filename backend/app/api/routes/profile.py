from fastapi import APIRouter, HTTPException
from backend.app.schemas.profile_schema import ProfileUpdateRequest, ProfileResponse
from backend.app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=ProfileResponse)
async def get_profile(user_id: int) -> ProfileResponse:
    """
    Get user profile, goal, and health metrics.
    """
    from backend.app.repositories.profile_repo import get_profile
    from backend.app.repositories.goal_repo import get_goal
    from backend.app.services.health_service import calculate_health_stats
    
    profile = get_profile(user_id)
    goal = get_goal(user_id)
    
    health_metrics = {"bmi": 0, "bmr": 0, "tdee": 0}
    if profile:
        health_metrics = calculate_health_stats({
            "weight": profile.get("weight_kg", 0),
            "height": profile.get("height_cm", 0),
            "age": profile.get("age", 25),
            "gender": profile.get("gender", "male"),
            "activity_level": profile.get("activity_level", "sedentary"),
        })
    
    return ProfileResponse(
        success=True,
        message="Profile retrieved successfully.",
        profile=profile,
        goal=goal,
        health_metrics=health_metrics
    )

@router.patch("/", response_model=ProfileResponse)
async def update_profile(body: ProfileUpdateRequest) -> ProfileResponse:
    """
    Update profile and goal. 
    Calculates TDEE and adjusts daily targets automatically.
    """
    # Convert Pydantic model to dict, excluding None for partial updates if needed
    # But our service handles None check.
    data = body.dict(exclude_unset=True)
    
    result = UserService.update_profile(body.user_id, data)
    
    return ProfileResponse(
        success=result["success"],
        message=result["message"],
        profile=result.get("profile"),
        goal=result.get("goal"),
        health_metrics=result.get("health_metrics")
    )
