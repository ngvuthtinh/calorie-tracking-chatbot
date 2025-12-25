from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.services.food_service import FoodService


def handle_food(intent: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch food intents to specific handlers.
    
    Args:
        intent: The intent name (e.g., 'log_food')
        data: The extracted data payload
        context: Context containing 'user_id' and 'date'
    """
    user_id = context.get("user_id")
    entry_date = context.get("date")

    if not user_id or not entry_date:
        return {
            "success": False,
            "message": "Missing user context (user_id or date).",
            "result": None
        }

    if intent == "log_food":
        return FoodService.log_food(user_id, entry_date, data)
    elif intent == "edit_food_entry":
        return FoodService.edit_food_entry(user_id, entry_date, data)
    elif intent == "add_food_items":
        return FoodService.add_food_items(user_id, entry_date, data)
    elif intent == "move_food_entry":
        return FoodService.move_food_entry(user_id, entry_date, data)
    elif intent == "delete_food_entry":
        return FoodService.delete_food_entry(user_id, entry_date, data)

    return {
        "success": False,
        "message": f"Unknown food intent: {intent}",
        "result": None
    }
