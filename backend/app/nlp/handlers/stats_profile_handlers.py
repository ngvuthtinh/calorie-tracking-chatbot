from typing import Any, Dict, List
from datetime import date, timedelta
from backend.app.repositories.stats_repo import get_day_logs, get_week_logs
from backend.app.repositories.profile_repo import upsert_profile
from backend.app.repositories.goal_repo import upsert_goal
from backend.app.repositories.profile_repo import get_profile

# Main handler
def handle_stats_profile(intent: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder for stats and profile intent handler.
    
    Args:
        intent: The stats/profile intent name
        data: Parsed data from the semantic visitor
        context: Context dict containing user_id and date
        
    Returns:
        Dict with 'message' and optional 'result' keys
    """
    if intent == "show_summary_today":
        return _handle_summary_today(context)
    elif intent == "show_summary_date":
        return _handle_summary_date(data, context)
    elif intent in ("show_weekly_stats", "show_stats_this_week"):
        return _handle_weekly_stats(context)
    elif intent == "update_profile":
        return _handle_update_profile(data, context)
    elif intent == "undo":
        return _handle_undo(data, context)
    else:
        return {"success": False, "message": f"Unknown stats/profile intent: {intent}", "result": None}

# Utility functions
def _get_day_session(context: Dict[str, Any], day: date = None) -> Dict[str, Any]:
    """
    Get or initialize the session data for a selected day.
    """
    if day is None:
        day = context.get("date")
    if "day_sessions" not in context:
        context["day_sessions"] = {}
    day_str = day.isoformat()
    if day_str not in context["day_sessions"]:
        context["day_sessions"][day_str] = {
            "food_entries": [],
            "exercise_entries": [],
            "profile": {},
            "history": []
        }
    return context["day_sessions"][day_str]


def _format_summary(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "No entries for this day."
    lines = []
    for i, e in enumerate(entries, 1):
        if "type" in e:
            desc = e["type"]
            if "calories" in e:
                desc += f" ({e['calories']} kcal)"
            lines.append(f"{i}. {desc}")
        elif "items" in e:  # exercise
            items_desc = []
            for item in e["items"]:
                t = item.get("type", "unknown")
                if "duration_min" in item:
                    items_desc.append(f"{t} {item['duration_min']}min")
                elif "distance_km" in item:
                    items_desc.append(f"{t} {item['distance_km']}km")
                elif "reps" in item:
                    items_desc.append(f"{item['reps']} {t}")
            lines.append(f"{i}. {', '.join(items_desc)}")
    return "\n".join(lines)


# Stats handlers
def _handle_summary_today(context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    day = context["date"]

    logs = get_day_logs(user_id, day)

    food_entries = logs["food_entries"]
    exercise_entries = logs["exercise_entries"]

    food_summary = _format_summary(food_entries)
    exercise_summary = _format_summary(exercise_entries)

    message = (
        f"Summary for {day.isoformat()}:\n\n"
        f"Food:\n{food_summary}\n\n"
        f"Exercise:\n{exercise_summary}"
    )

    return {
        "success": True,
        "message": message,
        "result": logs
    }


def _handle_summary_date(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    day = data["date"]
    if isinstance(day, str):
        day = date.fromisoformat(day)

    logs = get_day_logs(user_id, day)

    food_summary = _format_summary(logs["food_entries"])
    exercise_summary = _format_summary(logs["exercise_entries"])

    message = (
        f"Summary for {day.isoformat()}:\n\n"
        f"Food:\n{food_summary}\n\n"
        f"Exercise:\n{exercise_summary}"
    )

    return {
        "success": True,
        "message": message,
        "result": logs
    }


def _handle_weekly_stats(context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    end_date = context["date"]
    start_date = end_date - timedelta(days=6)

    week_logs = get_week_logs(user_id, start_date, end_date)

    total_food = []
    total_exercise = []

    for day in week_logs:
        total_food.extend(day["food_entries"])
        total_exercise.extend(day["exercise_entries"])

    message = (
        f"Weekly summary ({start_date.isoformat()} → {end_date.isoformat()}):\n"
        f"Food entries: {len(total_food)}\n"
        f"Exercise entries: {len(total_exercise)}"
    )

    return {
        "success": True,
        "message": message,
        "result": {
            "days": week_logs,
            "food_entries": total_food,
            "exercise_entries": total_exercise,
        }
    }


# Profile handler
def _handle_update_profile(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    field = data.get("field")
    value = data.get("value")
    unit = data.get("unit")

    if not field or value is None:
        return {"success": False, "message": "Missing field or value", "result": None}

    session = _get_day_session(context)
    profile = session["profile"]
    user_id = context["user_id"]

    # ---------- GOAL AUTO INFERENCE ----------
    if field == "goal" and value == "auto":
        target_weight = data.get("target_weight")
        if not target_weight:
            return {"success": False, "message": "Missing target weight", "result": None}

        profile_db = get_profile(user_id)
        current_weight = profile_db["weight_kg"] if profile_db and profile_db.get("weight_kg") else 0

        from backend.app.services.goal_service import infer_goal_from_target
        goal_type, delta = infer_goal_from_target(current_weight, target_weight)

        profile["goal"] = goal_type
        profile["target_weight"] = target_weight
        profile["target_delta"] = delta

    else:
        profile[field] = f"{value} {unit}" if unit else value

    # ---------- SAVE PROFILE ----------
    def extract_val(v):
        if isinstance(v, (int, float)):
            return v
        if isinstance(v, str):
            return float(v.split()[0])
        return None

    if field == "height":
        upsert_profile(user_id, height_cm=extract_val(value))
    elif field == "weight":
        upsert_profile(user_id, weight_kg=extract_val(value))
    elif field == "age":
        upsert_profile(user_id, age=int(value))
    elif field == "gender":
        upsert_profile(user_id, gender=value)
    elif field == "activity_level":
        upsert_profile(user_id, activity_level=value)

    # ---------- SAVE GOAL ----------
    if "goal" in profile:
        from backend.app.services.goal_service import calculate_daily_target

        GOAL_DB_MAP = {
            "lose_weight": "lose",
            "maintain_weight": "maintain",
            "gain_weight": "gain"
        }

        goal_type = profile["goal"]
        goal_type_db = GOAL_DB_MAP[goal_type]

        has_basics = all(k in profile for k in ["weight", "height", "age", "gender"])
        daily_target = None

        if has_basics:
            stats = calculate_health_stats(profile)
            daily_target = calculate_daily_target(stats["tdee"], goal_type)

        upsert_goal(
            user_id=user_id,
            goal_type=goal_type_db,
            target_weight_kg=profile.get("target_weight"),
            target_delta_kg=profile.get("target_delta"),
            daily_target_kcal=daily_target
        )

    return {
        "success": True,
        "message": f"Updated profile: {field}",
        "result": profile
    }


# Undo handler
def _handle_undo(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    session = _get_day_session(context)
    history = session.get("history", [])
    if not history:
        return {"success": False, "message": "Nothing to undo.", "result": None}

    last_action = history.pop()
    removed = None
    if "food" in last_action:
        removed = session["food_entries"].pop() if session["food_entries"] else None
    elif "exercise" in last_action:
        removed = session["exercise_entries"].pop() if session["exercise_entries"] else None

    return {
        "success": True, 
        "message": "Undid last action for this day.", 
        "result": removed
    }