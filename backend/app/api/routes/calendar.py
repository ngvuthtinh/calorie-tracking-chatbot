from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.calendar_schema import (
    DayViewResponse, 
    MonthViewResponse, 
    DaySummary,
    LogEntry
)

router = APIRouter()

# --- Endpoints ---
@router.get("/day/{entry_date}", response_model=DayViewResponse)
async def get_day_view(
    entry_date: str,
    user_id: int = Query(..., description="User ID")
) -> DayViewResponse:
    """
    Get daily log + summary.
    """
    # Placeholder
    return DayViewResponse(
        date=entry_date,
        food_entries=[],
        exercise_entries=[],
        summary=DaySummary(
            intake_kcal=0, burned_kcal=0, net_kcal=0, 
            target_kcal=2000, remaining_kcal=2000
        )
    )

@router.get("/calendar/month", response_model=MonthViewResponse)
async def get_month_view(
    user_id: int = Query(..., description="User ID"),
    month: str = Query(..., description="YYYY-MM")
) -> MonthViewResponse:
    """
    Get monthly status (dots/heatmap).
    """
    # Placeholder
    return MonthViewResponse(month=month, days=[])
