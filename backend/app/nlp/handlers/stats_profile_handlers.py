from typing import Any, Dict, List
from datetime import date, timedelta
from backend.app.repositories.stats_repo import get_day_logs, get_week_logs
from backend.app.repositories.profile_repo import upsert_profile

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
    
    # Handle "auto" goal (set goal 60 kg)
    if field == "goal" and value == "auto":
        # We need target_weight and current weight
        if "target_weight" in data:
            t_weight = data["target_weight"]
            session["profile"]["target_weight"] = t_weight
            
            # Try to get current weight
            c_weight_str = session["profile"].get("weight", "0")
            try:
                c_weight = float(c_weight_str.split()[0])
            except (ValueError, IndexError):
                c_weight = 0
            
            from backend.app.services.goal_service import infer_goal_from_target
            value, delta = infer_goal_from_target(c_weight, t_weight)
            data["target_delta"] = delta
            
            # Update data/session for consistency
            session["profile"]["goal"] = value

    session["profile"][field] = f"{value} {unit}" if unit else value
    
    # Store extra goal data if present
    if "target_delta" in data:
        session["profile"]["target_delta"] = data["target_delta"]
    
    try:
        from backend.app.repositories.users_repo import update_user_profile, update_user_goal
        user_id = context.get("user_id")
        if user_id:
            # 1. Prepare Profile Data
            def extract_val(val_str):
                if isinstance(val_str, (int, float)): return val_str
                if not isinstance(val_str, str): return None
                return float(val_str.split()[0])
            
            p_data = session["profile"]
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
            update_user_profile(user_id, profile_db)
            
            # 2. Prepare Goal Data (if goal exists)
            if "goal" in p_data:
                goal_db = {
                    "goal_type": p_data.get("goal"),
                    "target_weight_kg": p_data.get("target_weight"),
                    "target_delta_kg": p_data.get("target_delta"),
                    "daily_target_kcal": None 
                }
                if has_basics:
                    if not stats: stats = calculate_health_stats(profile)
                    from backend.app.services.goal_service import calculate_daily_target
                    target = calculate_daily_target(stats['tdee'], p_data["goal"])
                    goal_db["daily_target_kcal"] = target
                    
                update_user_goal(user_id, goal_db)
                
    except Exception as e:
        print(f"[Warning] Failed to save profile to DB: {e}")

    profile = session["profile"]
    has_basics = all(k in profile for k in ["weight", "height", "age", "gender"])
    
    stats_msg = ""
    if has_basics:
        stats = calculate_health_stats(profile)
        if stats['bmi'] > 0:
            stats_msg = f"\n\n[Health Update]\nBMI: {stats['bmi']}\nBMR: {stats['bmr']} kcal\nTDEE: {stats['tdee']} kcal"
            
            # Add target if goal exists
            if "goal" in profile:
                from backend.app.services.goal_service import calculate_daily_target
                tdee = stats['tdee']
                target = calculate_daily_target(tdee, profile["goal"])
                
                goal_str = profile["goal"]
                if "target_delta" in profile:
                    goal_str += f" {profile['target_delta']} {profile.get('target_unit', 'kg')}"
                
                stats_msg += f"\nDaily Target: {target} kcal ({goal_str})"

    return {
        "success": True, 
        "message": f"Updated profile: {field} = {session['profile'][field]}{stats_msg}", 
        "result": session["profile"]
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