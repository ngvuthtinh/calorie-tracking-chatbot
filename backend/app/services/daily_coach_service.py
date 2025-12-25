from typing import Dict, Any, List

def daily_coach_summary(intake_kcal: int, burned_kcal: int, target_kcal: int) -> dict:
    """
    Combine intake, burned, and target calories
    to produce daily progress feedback.
    """

    net_kcal = intake_kcal - burned_kcal
    remaining = target_kcal - net_kcal

    if remaining > 0:
        status = "on_track"
        message = f"You can still gain {remaining} kcal today."
    elif remaining < 0:
        status = "over"
        message = f"You are over your target by {abs(remaining)} kcal."
    else:
        status = "on_track"
        message = "You have exactly met your calorie target today."

    return {
        "intake_kcal": intake_kcal,
        "burned_kcal": burned_kcal,
        "target_kcal": target_kcal,
        "net_kcal": net_kcal,
        "remaining_kcal": remaining,
        "status": status,
        "message": message
    }