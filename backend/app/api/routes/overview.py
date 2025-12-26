from fastapi import APIRouter, Query
from backend.app.schemas.calendar_schema import OverviewStats
from backend.app.services.stats_service import StatsService

router = APIRouter()

@router.get("/", response_model=OverviewStats)
async def get_overview(
    user_id: int = Query(..., description="User ID")
) -> OverviewStats:
    """
    Get home overview stats.
    (Total streak, weight progress, etc.)
    """
    stats = StatsService.get_overview_stats(user_id)
    return OverviewStats(**stats)
