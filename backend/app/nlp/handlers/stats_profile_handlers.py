from typing import Any, Dict, List
from datetime import date, timedelta
from decimal import Decimal
from backend.app.repositories.stats_repo import get_day_logs, get_week_logs
from backend.app.repositories.profile_repo import get_profile, upsert_profile
from backend.app.repositories.goal_repo import get_goal, upsert_goal
from backend.app.services.health_service import calculate_health_stats
from backend.app.services.goal_service import infer_goal_from_target, calculate_daily_target

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

    profile = get_profile(user_id)
    goal = get_goal(user_id)

    stats_msg = ""
    if profile:
        stats = calculate_health_stats({
            "weight": profile["weight_kg"],
            "height": profile["height_cm"],
            "age": profile["age"],
            "gender": profile["gender"],
            "activity_level": profile["activity_level"],
        })

        stats_msg += (
            f"\n\nHealth:\n"
            f"BMI: {stats['bmi']}\n"
            f"BMR: {stats['bmr']} kcal\n"
            f"TDEE: {stats['tdee']} kcal"
        )

        if goal and goal.get("daily_target_kcal") is not None:
            stats_msg += (
                f", Daily target: {goal['daily_target_kcal']} kcal "
                f"({goal['goal_type']})"
            )
        else:
            stats_msg += f"\nGoal: {goal['goal_type']} (target not calculated yet)"

    message = (
        f"Summary for {day}:\n\n"
        f"Food:\n{_format_summary(logs['food_entries'])}\n\n"
        f"Exercise:\n{_format_summary(logs['exercise_entries'])}"
        f"{stats_msg}"
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
    field = data["field"]
    value = data["value"]
    user_id = context["user_id"]
    
    # Get or init session for today
    if "day_sessions" not in context:
        context["day_sessions"] = {}
    session = context["day_sessions"].setdefault("profile_session", {"profile": {}, "history": []})

    def extract_val(val):
        if isinstance(val, (int, float, Decimal)):
            return float(val)
        try:
            return float(str(val).split()[0])
        except Exception:
            return 0.0

    # --- GOAL AUTO UPDATE ---
    if field == "goal" and value == "auto":
        target_weight = extract_val(data.get("target_weight", 0))
        profile_db = get_profile(user_id)
        if not profile_db or not profile_db.get("weight_kg"):
            return {"success": False, "message": "Please set your weight before setting a goal."}

        # Infer goal type and delta
        goal_type, delta = infer_goal_from_target(float(profile_db["weight_kg"]), target_weight)

        # Calculate daily target using target weight
        profile_for_stats = {**profile_db, "weight_kg": target_weight}
        stats = calculate_health_stats({
            "weight": profile_for_stats["weight_kg"],
            "height": profile_for_stats["height_cm"],
            "age": profile_for_stats["age"],
            "gender": profile_for_stats["gender"],
            "activity_level": profile_for_stats["activity_level"],
        })
        daily_target = calculate_daily_target(stats["tdee"], goal_type)

        # Upsert goal
        upsert_goal(
            user_id=user_id,
            goal_type=goal_type,
            target_weight_kg=target_weight,
            target_delta_kg=delta,
            daily_target_kcal=daily_target,
        )

        # Update session
        session["profile"].update({
            "goal": goal_type,
            "target_weight": target_weight,
            "target_delta": delta,
            "daily_target_kcal": daily_target
        })

        msg = f"Updated goal: {goal_type}, Daily target: {daily_target} kcal"
        return {"success": True, "message": msg, "result": session["profile"]}

    # --- PROFILE UPDATE ---
    kwargs = {}
    if field == "weight":
        val = extract_val(value)
        kwargs["weight_kg"] = val
        session["profile"][field] = val
    elif field == "height":
        val = extract_val(value)
        kwargs["height_cm"] = val
        session["profile"][field] = val
    elif field == "age":
        val = int(extract_val(value))
        kwargs["age"] = val
        session["profile"][field] = val
    elif field == "gender":
        kwargs["gender"] = value
        session["profile"][field] = value
    elif field == "activity_level":
        kwargs["activity_level"] = value
        session["profile"][field] = value

    if kwargs:
        upsert_profile(user_id, **kwargs)

    # Recalculate daily target using **current weight** and existing goal
    profile_db = get_profile(user_id)
    goal_db = get_goal(user_id)
    daily_target = None
    if profile_db and goal_db and goal_db.get("goal_type"):
        stats = calculate_health_stats({
            "weight": profile_db["weight_kg"],
            "height": profile_db["height_cm"],
            "age": profile_db["age"],
            "gender": profile_db["gender"],
            "activity_level": profile_db["activity_level"],
        })
        daily_target = calculate_daily_target(stats["tdee"], goal_db["goal_type"])
        upsert_goal(user_id=user_id, goal_type=goal_db["goal_type"], daily_target_kcal=daily_target)
        session["profile"]["daily_target_kcal"] = daily_target

    return {
        "success": True,
        "message": f"Updated profile: {field} = {value}, Daily target: {daily_target if daily_target else 0} kcal",
        "result": session["profile"],
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