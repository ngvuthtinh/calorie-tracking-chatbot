from typing import Any, Dict, List
from datetime import date, timedelta
from app.services.daily_coach_service import daily_coach_summary

# MAIN ENTRY
def handle_stats_profile(intent: str, data: Dict[str, Any], context: Dict[str, Any]):
    selected_date = context["date"]

    # STATS
    if intent == "show_summary_today":
        stats = _build_daily_stats(context, selected_date)
        return {"success": True, "results": [_format_daily_message(stats)]}

    if intent == "show_summary_date":
        target = date.fromisoformat(data["date"])
        stats = _build_daily_stats(context, target)
        return {"success": True, "results": [_format_daily_message(stats)]}

    if intent in ("show_weekly_stats", "show_stats_this_week"):
        stats = _build_weekly_stats(context, selected_date)
        return {"success": True, "results": [_format_weekly_message(stats)]}

    # PROFILE
    if intent == "update_profile":
        return _handle_profile(data, context)

    # UNDO
    if intent == "undo":
        return _handle_undo(context)

    return {"success": False, "error": f"Unknown stats/profile command: {intent}"}

# SESSION STORAGE
def _get_day_session(context: Dict[str, Any], day: date = None) -> Dict[str, Any]:
    if day is None:
        day = context["date"]
    if "day_sessions" not in context:
        context["day_sessions"] = {}
    key = day.isoformat()
    if key not in context["day_sessions"]:
        context["day_sessions"][key] = {
            "food_entries": [],
            "exercise_entries": [],
            "profile": {},
            "history": []
        }
    return context["day_sessions"][key]


# STATS HELPERS
def _filter_by_date(entries: List[Dict[str, Any]], target_date: date) -> List[Dict[str, Any]]:
    return [e for e in entries if e.get("entry_date") == target_date]

def _sum_calories(entries: List[Dict[str, Any]]) -> int:
    return sum(e.get("calories", 0) for e in entries)

def _build_daily_stats(context: Dict[str, Any], target_date: date) -> Dict[str, Any]:
    session = _get_day_session(context, target_date)
    food_entries = _filter_by_date(session.get("food_entries", []), target_date)
    exercise_entries = _filter_by_date(session.get("exercise_entries", []), target_date)
    intake = _sum_calories(food_entries)
    burned = _sum_calories(exercise_entries)
    target_kcal = context.get("target_kcal", 2000)
    coach = daily_coach_summary(intake, burned, target_kcal)
    return {"date": target_date.isoformat(), **coach}

def _build_weekly_stats(context: Dict[str, Any], end_date: date) -> Dict[str, Any]:
    total_intake = 0
    total_burned = 0
    daily_stats = []
    for i in range(7):
        day = end_date - timedelta(days=i)
        session = _get_day_session(context, day)
        food = _filter_by_date(session.get("food_entries", []), day)
        exercise = _filter_by_date(session.get("exercise_entries", []), day)
        intake = _sum_calories(food)
        burned = _sum_calories(exercise)
        total_intake += intake
        total_burned += burned
        daily_stats.append({"date": day.isoformat(), "intake_kcal": intake, "burned_kcal": burned})
    return {
        "start_date": (end_date - timedelta(days=6)).isoformat(),
        "end_date": end_date.isoformat(),
        "total_intake_kcal": total_intake,
        "total_burned_kcal": total_burned,
        "daily": daily_stats
    }

def _format_daily_message(stats: Dict[str, Any]) -> str:
    return (
        f"Summary for {stats['date']}:\n"
        f"- Intake: {stats['intake_kcal']} kcal\n"
        f"- Burned: {stats['burned_kcal']} kcal\n"
        f"- Net: {stats['net_kcal']} kcal\n"
        f"- {stats['message']}"
    )

def _format_weekly_message(stats: Dict[str, Any]) -> str:
    return (
        f"Weekly summary ({stats['start_date']} → {stats['end_date']}):\n"
        f"- Total intake: {stats['total_intake_kcal']} kcal\n"
        f"- Total burned: {stats['total_burned_kcal']} kcal"
    )

# PROFILE HANDLER
def _handle_profile(data: Dict[str, Any], context: Dict[str, Any]):
    field = data.get("field")
    value = data.get("value")
    unit = data.get("unit")
    if not field or value is None:
        return {"success": False, "error": "Missing profile field or value"}
    session = _get_day_session(context)
    session["profile"][field] = f"{value}{unit}" if unit else value
    session["history"].append({"type": "profile", "field": field})
    
    if field == "weight": context["weight_kg"] = float(value)
    if field == "height": context["height_cm"] = int(value)
    if field == "activity_level": context["activity_level"] = value
    if field == "goal": context["goal"] = value
    return {"success": True, "results": [f"Updated profile: {field} = {session['profile'][field]}"]}

# UNDO HANDLER
def _handle_undo(context: Dict[str, Any]):
    session = _get_day_session(context)
    history = session["history"]
    if not history:
        return {"success": False, "error": "Nothing to undo"}
    last = history.pop()
    if last["type"] == "profile":
        field = last["field"]
        session["profile"].pop(field, None)
        return {"success": True, "results": [f"Undid profile update: {field}"]}
    if last["type"] == "food":
        session["food_entries"].pop()
    if last["type"] == "exercise":
        session["exercise_entries"].pop()
    return {"success": True, "results": ["Undid last action"]}
