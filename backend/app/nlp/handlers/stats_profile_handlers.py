from typing import Any, Dict, List
from datetime import date, timedelta
from datetime import date, timedelta
from backend.app.services.user_service import UserService
from backend.app.services.stats_service import StatsService
from backend.app.services.action_service import ActionService


# Main handler
def handle_stats_profile(intent: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for stats and profile intents.
    """
    if intent == "show_summary_today":
        return _handle_summary_today(context)
    elif intent == "show_summary_date":
        return _handle_summary_date(data, context)
    elif intent == "show_weekly_stats":
        return _handle_weekly_stats(context)
    elif intent == "show_stats_this_week":
        return _handle_stats_this_week(context)
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


# Stats handlers
def _handle_summary_today(context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    day = context["date"]
    
    return StatsService.get_summary_today(user_id, day)


def _handle_summary_date(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    day = data["date"]
    if isinstance(day, str):
        day = date.fromisoformat(day)
        
    return StatsService.get_summary_date(user_id, day)


    user_id = context["user_id"]
    end_date = context["date"]
    return StatsService.get_weekly_stats(user_id, end_date)

def _handle_stats_this_week(context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    today = context["date"]
    return StatsService.get_stats_this_week(user_id, today)


# Profile handler
def _handle_update_profile(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    
    # Delegate to Service
    response = UserService.update_profile(user_id, data)
    
    # Update local context if successful (to keep session in sync? Legacy compatibility)
    if response["success"] and response["result"]:
        # Get or init session for today
        if "day_sessions" not in context:
            context["day_sessions"] = {}
        session = context["day_sessions"].setdefault("profile_session", {"profile": {}, "history": []})
        
        # Merge updates
        session["profile"].update(response["result"])
        
    return response


# Undo handler
def _handle_undo(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context.get("user_id")
    date_obj = context.get("date")
    date_str = str(date_obj)
    scope = data.get("scope")
    
    return ActionService.undo_last_action(user_id, date_str, scope)
