from fastapi import APIRouter, Query
from backend.app.schemas.calendar_schema import OverviewStats

router = APIRouter()

@router.get("/", response_model=OverviewStats)
async def get_overview(
    user_id: int = Query(..., description="User ID")
) -> OverviewStats:
    """
    Get home overview stats.
    (Total streak, weight progress, etc.)
    """
    # Placeholder Logic
    return OverviewStats(
        total_days_logged=0,
        current_streak=0,
        weight_start=0.0,
        weight_current=0.0,
        start_date="2023-01-01"
    )
