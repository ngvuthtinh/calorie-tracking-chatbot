from typing import Dict, Any
from app.services.daily_coach_service import daily_coach_summary

def build_daily_stats(day_session: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate intake, burned, and target calories for one day.
    """

    intake = 0
    burned = 0
    target = day_session.get("profile", {}).get("target_kcal", 2000)

    # Sum food calories
    for f in day_session.get("food_entries", []):
        intake += f.get("calories", 0)

    # Sum exercise calories
    for e in day_session.get("exercise_entries", []):
        burned += e.get("calories", 0)

    return daily_coach_summary(
        intake_kcal=intake,
        burned_kcal=burned,
        target_kcal=target
    )
