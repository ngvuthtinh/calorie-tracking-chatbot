from fastapi import APIRouter, Query
from backend.app.schemas.calendar_schema import OverviewStats
from backend.app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=OverviewStats)
async def get_overview(
    user_id: int = Query(..., description="User ID")
) -> OverviewStats:
    """
    Get home overview stats.
    (Total streak, weight progress, etc.)
    """
    stats = UserService.get_overview_stats(user_id)
    return OverviewStats(**stats)
