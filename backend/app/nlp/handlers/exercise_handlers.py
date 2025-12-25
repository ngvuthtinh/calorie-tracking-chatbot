from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.services.exercise_service import ExerciseService


def handle_exercise(intent: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main router for exercise intents.
    """
    user_id = context.get("user_id")
    entry_date = context.get("date")
    
    if not user_id or not entry_date:
        return {
            "success": False,
            "message": "Missing user context (user_id or date).",
            "result": None
        }
    
    if intent == "log_exercise":
        return ExerciseService.log_exercise(user_id, entry_date, data, context)
    elif intent == "edit_exercise_entry":
        return ExerciseService.edit_exercise_entry(user_id, entry_date, data, context)
    elif intent == "edit_exercise_item":
        return ExerciseService.edit_exercise_item(user_id, entry_date, data, context)
    elif intent == "add_exercise_items":
        return ExerciseService.add_exercise_items(user_id, entry_date, data, context)
    elif intent == "delete_exercise_entry":
        return ExerciseService.delete_exercise_entry(user_id, entry_date, data)
    else:
        return {"success": False, "message": f"Unknown exercise intent: {intent}", "result": None}
