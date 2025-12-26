from fastapi import APIRouter, Query
from datetime import date

from backend.app.services.user_service import UserService
from backend.app.schemas.calendar_schema import (
    DayViewResponse, DaySummary, LogEntry,
    MonthViewResponse, MonthDayStatus
)

router = APIRouter()


# ----------------- DAY VIEW -----------------
@router.get("/day/{entry_date}", response_model=DayViewResponse)
def get_day_view(entry_date: date):
    """
    Get detailed day view with food/exercise entries and summary.
    
    Returns comprehensive daily nutrition data including:
    - Individual food entries with calories (uses pre-calculated intake_kcal from DB)
    - Individual exercise entries with calories burned
    - Daily summary: total intake, burned, net calories, target, and remaining
    
    Note: This endpoint reuses existing DB calculations (intake_kcal, burned_kcal)
    rather than recalculating from catalog to ensure consistency with logged data.
    
    Args:
        entry_date: Date to retrieve data for (YYYY-MM-DD format)
        
    Returns:
        DayViewResponse with date, summary, food_entries, and exercise_entries
    """
    # Delegate to UserService which handles all business logic
    result = UserService.get_day_view_api(user_id=1, entry_date=entry_date)
    
    # Convert dict to Pydantic models for API response validation
    return DayViewResponse(
        date=result["date"],
        summary=DaySummary(**result["summary"]),
        food_entries=[LogEntry(**entry) for entry in result["food_entries"]],
        exercise_entries=[LogEntry(**entry) for entry in result["exercise_entries"]],
        coach_advice=result.get("coach_advice")
    )


# ----------------- MONTH VIEW -----------------
@router.get("/calendar/month", response_model=MonthViewResponse)
def get_month_view(month: str = Query(..., description="YYYY-MM")):
    """
    Get month view with daily status for all days in the month.
    
    Returns aggregated daily statistics for an entire month:
    - Each day shows: date, status (under/over budget), net calories
    - Status is calculated as: net_kcal <= target_kcal ? "under_budget" : "over_budget"
    - Uses efficient SQL aggregation via get_period_stats() repository function
    
    Args:
        month: Month to retrieve in YYYY-MM format (e.g., "2025-12")
        
    Returns:
        MonthViewResponse with month string and list of daily status objects
    """
    # Delegate to UserService which uses get_period_stats for efficient aggregation
    result = UserService.get_month_view_api(user_id=1, month=month)
    
    # Convert dict to Pydantic models for API response validation
    return MonthViewResponse(
        month=result["month"],
        days=[MonthDayStatus(**day) for day in result["days"]]
    )