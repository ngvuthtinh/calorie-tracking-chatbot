from typing import Dict, Any, List
from datetime import date, timedelta
from app.services.daily_coach_service import daily_coach_summary


# helpers
def _filter_by_date(entries: List[Dict[str, Any]], target_date: date) -> List[Dict[str, Any]]:
    return [
        e for e in entries
        if e.get("entry_date") == target_date
    ]

def _sum_calories(entries: List[Dict[str, Any]]) -> int:
    return sum(e.get("calories", 0) for e in entries)

# daily stats
def build_daily_stats(context: Dict[str, Any], target_date: date) -> Dict[str, Any]:
    food_entries = context.get("food_entries", [])
    exercise_entries = context.get("exercise_entries", [])

    day_food = _filter_by_date(food_entries, target_date)
    day_exercise = _filter_by_date(exercise_entries, target_date)

    intake = _sum_calories(day_food)
    burned = _sum_calories(day_exercise)

    target_kcal = context.get("target_kcal", 2000)

    coach = daily_coach_summary(
        intake_kcal=intake,
        burned_kcal=burned,
        target_kcal=target_kcal
    )

    return {
        "date": target_date.isoformat(),
        "intake_kcal": intake,
        "burned_kcal": burned,
        **coach
    }

# weekly stats
def build_weekly_stats(context: Dict[str, Any], end_date: date) -> Dict[str, Any]:
    food_entries = context.get("food_entries", [])
    exercise_entries = context.get("exercise_entries", [])

    start_date = end_date - timedelta(days=6)

    daily = []
    total_intake = 0
    total_burned = 0

    for i in range(7):
        day = start_date + timedelta(days=i)

        day_food = _filter_by_date(food_entries, day)
        day_exercise = _filter_by_date(exercise_entries, day)

        intake = _sum_calories(day_food)
        burned = _sum_calories(day_exercise)

        total_intake += intake
        total_burned += burned

        daily.append({
            "date": day.isoformat(),
            "intake_kcal": intake,
            "burned_kcal": burned
        })

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_intake_kcal": total_intake,
        "total_burned_kcal": total_burned,
        "daily": daily
    }
