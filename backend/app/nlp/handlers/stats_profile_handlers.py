"""
Stats and Profile Handlers Module (Placeholder)

TODO: Implement stats and profile-related intent handlers.
"""

from typing import Any, Dict, List
from datetime import date, timedelta

# Main handler
def handle_stats_profile(intent: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder for stats and profile intent handler.
    
    Args:
        intent: The stats/profile intent name
        data: Parsed data from the semantic visitor
        repo: Repository access object
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
    session = _get_day_session(context)
    food_summary = _format_summary(session.get("food_entries", []))
    exercise_summary = _format_summary(session.get("exercise_entries", []))
    message = f"Summary for {context['date'].isoformat()}:\n\nFood:\n{food_summary}\n\nExercise:\n{exercise_summary}"
    return {
        "success": True, 
        "message": message, 
        "result": {
            "food_entries": session["food_entries"], 
            "exercise_entries": session["exercise_entries"]
        }
    }


def _handle_summary_date(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    day = data.get("date")
    if isinstance(day, str):
        day = date.fromisoformat(day)
    session = _get_day_session(context, day)
    food_summary = _format_summary(session.get("food_entries", []))
    exercise_summary = _format_summary(session.get("exercise_entries", []))
    message = f"Summary for {day.isoformat()}:\n\nFood:\n{food_summary}\n\nExercise:\n{exercise_summary}"
    return {
        "success": True, 
        "message": message, 
        "result": {
            "food_entries": session["food_entries"], 
            "exercise_entries": session["exercise_entries"]
        }
    }


def _handle_weekly_stats(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate stats for the last 7 days including the selected date.
    """
    today = context.get("date")
    week_summary = {"food_entries": [], "exercise_entries": []}

    if "day_sessions" not in context or not context["day_sessions"]:
        return {"success": True, "message": "No entries this week.", "result": week_summary}

    for i in range(7):
        day = today - timedelta(days=i)
        session = context["day_sessions"].get(day.isoformat())
        if session:
            week_summary["food_entries"].extend(session.get("food_entries", []))
            week_summary["exercise_entries"].extend(session.get("exercise_entries", []))

    message = (
        f"Weekly summary (last 7 days including {today.isoformat()}):\n"
        f"Food: {len(week_summary['food_entries'])} entries\n"
        f"Exercise: {len(week_summary['exercise_entries'])} entries"
    )
    return {"success": True, "message": message, "result": week_summary}


# Profile handler
def _handle_update_profile(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    field = data.get("field")
    value = data.get("value")
    unit = data.get("unit")
    if not field or value is None:
        return {"success": False, "message": "Missing field or value", "result": None}

    session = _get_day_session(context)
    session["profile"][field] = f"{value} {unit}" if unit else value
    return {
        "success": True, 
        "message": f"Updated profile: {field} = {session['profile'][field]}", 
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
