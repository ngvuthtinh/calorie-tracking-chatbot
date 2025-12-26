from typing import Any, Dict, List
from datetime import date, timedelta
from backend.app.services.user_service import UserService


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
    
    return UserService.get_summary_today(user_id, day)


def _handle_summary_date(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    day = data["date"]
    if isinstance(day, str):
        day = date.fromisoformat(day)
        
    return UserService.get_summary_date(user_id, day)


def _handle_weekly_stats(context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    end_date = context["date"]
    return UserService.get_weekly_stats(user_id, end_date)

def _handle_stats_this_week(context: Dict[str, Any]) -> Dict[str, Any]:
    user_id = context["user_id"]
    today = context["date"]
    return UserService.get_stats_this_week(user_id, today)


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
    from backend.app.repositories import action_log_repo, food_repo, exercise_repo
    
    user_id = context.get("user_id")
    date_obj = context.get("date")
    date_str = str(date_obj)
    
    # Determine scope filter
    scope = data.get("scope") # 'food' or 'exercise' or None
    table_filter = None
    if scope == "food":
        table_filter = "food_entry"
    elif scope == "exercise":
        table_filter = "exercise_entry"
        
    # Get last action
    last_action = action_log_repo.get_last_action(user_id, date_str, table_filter)
    
    if not last_action:
        msg = "Nothing to undo for today"
        if scope:
            msg += f" in {scope} category"
        return {"success": False, "message": msg + ".", "result": None}
        
    action_type = last_action["action_type"]
    ref_id = last_action["ref_id"]
    
    undone_item = None
    
    # Perform undo
    if action_type == "create_food":
        food_repo.delete_food_entry_by_id(ref_id)
        undone_item = "food entry"
    elif action_type == "create_exercise":
        exercise_repo.delete_exercise_entry_by_id(ref_id)
        undone_item = "exercise entry"
    else:
        # Unknown or unsupported action type (e.g. edit/delete actions might be logged but not simple to undo yet)
        # For MVP, we might only support undoing create actions, or we check action type.
        # If we logged 'edit_food', undoing it is harder (need previous state).
        # For now, let's assume we only undo 'create' actions safely.
        return {"success": False, "message": f"Cannot undo action of type '{action_type}'.", "result": None}
        
    # Remove the log entry so we don't undo it again (or can undo the one before it next time)
    action_log_repo.delete_log(last_action["id"])
    
    return {
        "success": True, 
        "message": f"Undid last action: {undone_item}.", 
        "result": {"undone_action": action_type, "ref_id": ref_id}
    }
