from fastapi import APIRouter, HTTPException
from backend.app.schemas.profile_schema import ProfileUpdateRequest, ProfileResponse

router = APIRouter()

@router.patch("/", response_model=ProfileResponse)
async def update_profile(body: ProfileUpdateRequest) -> ProfileResponse:
    """
    Update profile and goal.
    """
    # Placeholder
    return ProfileResponse(
        success=True,
        message="Profile updated",
        profile={},
        goal={},
        health_metrics={}
    )
