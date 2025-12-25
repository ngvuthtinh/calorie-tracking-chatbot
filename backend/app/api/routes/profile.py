from fastapi import APIRouter, HTTPException
from backend.app.schemas.profile_schema import ProfileUpdateRequest, ProfileResponse
from backend.app.services.user_service import UserService

router = APIRouter()

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
