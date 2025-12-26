from fastapi import APIRouter, Query
from datetime import date, timedelta
from backend.app.repositories.stats_repo import get_day_logs, get_week_logs, get_month_logs
from backend.app.repositories.goal_repo import get_goal
from backend.app.repositories.food_catalog_repo import FoodCatalogRepo
from backend.app.repositories.exercise_catalog_repo import ExerciseRepo
from backend.app.repositories.profile_repo import get_profile
from backend.app.schemas.calendar_schema import (
    DayViewResponse, DaySummary, LogEntry,
    MonthViewResponse, MonthDayStatus,
    WeekViewResponse, WeekDayStatus
)

router = APIRouter()

food_repo = FoodCatalogRepo()
exercise_repo = ExerciseRepo()

# ----------------- DAY VIEW -----------------
@router.get("/day/{entry_date}", response_model=DayViewResponse)
def get_day_view(entry_date: date):
    logs = get_day_logs(user_id=1, entry_date=entry_date)

    food_entries = []
    exercise_entries = []

    intake = 0.0
    burned = 0.0

    profile = get_profile(user_id=1)
    weight_kg = float(profile["weight_kg"]) if profile else 0.0

    # ---- FOOD ----
    for f in logs.get("food_entries", []):
        kcal_per_unit = food_repo.get_calories_per_unit(f["item_name"]) or 0.0

        qty = float(f.get("quantity") or 1.0)
        unit = f.get("unit")

        # If unit is grams and kcal is per 100g, divide by 100
        if unit == "g":
            kcal = kcal_per_unit * qty / 100
        else:
            kcal = kcal_per_unit * qty

        intake += kcal

        food_entries.append(
            LogEntry(
                id=f["id"],
                type="food",
                name=f["item_name"],
                calories=round(kcal),
                time=f.get("time"),
                quantity=qty,
                unit=unit,
            )
        )

    # ---- EXERCISE ----
    for x in logs.get("exercise_entries", []):
        met = float(x.get("met") or exercise_repo.get_met_value(x["name"]) or 0.0)
        duration_min = float(x.get("duration_min") or 0.0)
        exercise_weight = float(x.get("weight_kg") or weight_kg or 0.0)

        kcal = met * exercise_weight * (duration_min / 60)
        burned += kcal

        exercise_entries.append(
            LogEntry(
                id=x["id"],
                type="exercise",
                name=x["name"],
                calories=round(kcal),
                time=x.get("time"),
            )
        )

    net = intake - burned

    goal = get_goal(user_id=1)
    target = goal["daily_target_kcal"] if goal else 0
    remaining = target - net if target else 0

    summary = DaySummary(
        intake_kcal=round(intake),
        burned_kcal=round(burned),
        net_kcal=round(net),
        target_kcal=target,
        remaining_kcal=round(remaining),
    )

    return DayViewResponse(
        date=entry_date.isoformat(),
        summary=summary,
        food_entries=food_entries,
        exercise_entries=exercise_entries,
    )


# ----------------- WEEK VIEW -----------------
@router.get("/calendar/week", response_model=WeekViewResponse)
def get_week_view(date: str = Query(..., description="Any date in the week YYYY-MM-DD")):
    logs = get_week_logs(user_id=1, reference_date=date)
    days = []

    for d in logs:
        net = float(d["intake_kcal"]) - float(d["burned_kcal"])
        target = float(d["target_kcal"])
        status = "under_budget" if net <= target else "over_budget"

        days.append(
            WeekDayStatus(
                date=d["entry_date"].isoformat(),
                status=status,
                net_kcal=round(net),
            )
        )

    import datetime
    ref = datetime.date.fromisoformat(date)
    week_start = (ref - timedelta(days=ref.weekday())).isoformat()
    week_end = (ref + timedelta(days=6 - ref.weekday())).isoformat()

    return WeekViewResponse(
        week_start=week_start,
        week_end=week_end,
        days=days
    )


# ----------------- MONTH VIEW -----------------
@router.get("/calendar/month", response_model=MonthViewResponse)
def get_month_view(month: str):
    logs = get_month_logs(user_id=1, month=month)
    days = []

    for d in logs:
        net = float(d["intake_kcal"]) - float(d["burned_kcal"])
        target = float(d["target_kcal"])
        status = "under_budget" if net <= target else "over_budget"

        days.append(
            MonthDayStatus(
                date=d["entry_date"].isoformat(),
                status=status,
                net_kcal=round(net),
            )
        )

    return MonthViewResponse(
        month=month,
        days=days
    )