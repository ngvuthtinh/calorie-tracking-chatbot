from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.repositories import food_repo
from backend.app.services.nutrition_service import estimate_intake


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
        return _handle_log_food(data, user_id, entry_date)
    elif intent == "edit_food_entry":
        return _handle_edit_food_entry(data, user_id, entry_date)
    elif intent == "add_food_items":
        return _handle_add_food_items(data, user_id, entry_date)
    elif intent == "move_food_entry":
        return _handle_move_food_entry(data, user_id, entry_date)
    elif intent == "delete_food_entry":
        return _handle_delete_food_entry(data, user_id, entry_date)

    return {
        "success": False,
        "message": f"Unknown food intent: {intent}",
        "result": None
    }


def _handle_log_food(data: Dict[str, Any], user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'log_food': Create new food entries.
    Data schema: { "meal": str, "action": str, "items": [...] }
    """
    meal = data.get("meal", "snack")  # Default to snack if not specified
    items = data.get("items", [])
    
    if not items:
        return {"success": False, "message": "No food items to log.", "result": None}

    # Prepare entry structure
    entry = {
        "meal": meal,
        "items": items,
        "created_at_local": str(entry_date) 
    }

    # Repo interaction
    new_entry = food_repo.add_food_entry(user_id, entry_date, entry)

    # Calculate calories using nutrition service
    nutrition = estimate_intake(items)
    
    count = len(items)
    item_names = ", ".join([i.get("name", "food") for i in items])
    
    # Add nutrition info to result
    new_entry["nutrition"] = nutrition
    
    return {
        "success": True,
        "message": f"Logged {count} item(s) for {meal}: {item_names} ({nutrition['total_kcal']} kcal)",
        "result": new_entry
    }



def _handle_edit_food_entry(data: Dict[str, Any], user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'edit_food_entry': Overwrite/Update an existing entry.
    Data schema: { "entry_id": str, "meal": str, "items": [...] }
    """
    entry_id = data.get("entry_id")
    if not entry_id:
        return {"success": False, "message": "Missing entry ID for edit.", "result": None}

    # We update fields present in data
    updates = {}
    if "meal" in data:
        updates["meal"] = data["meal"]
    if "items" in data:
        updates["items"] = data["items"]

    updated_entry = food_repo.update_food_entry(user_id, entry_date, entry_id, updates)

    if not updated_entry:
         return {"success": False, "message": "Entry not found or could not be updated.", "result": None}

    return {
        "success": True,
        "message": "Food entry updated successfully.",
        "result": updated_entry
    }


def _handle_add_food_items(data: Dict[str, Any], user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'add_food_items': Append items to an existing entry.
    Data schema: { "entry_id": str, "items": [...] }
    """
    entry_id = data.get("entry_id")
    new_items = data.get("items", [])

    if not entry_id or not new_items:
        return {"success": False, "message": "Missing entry ID or items to add.", "result": None}
    
    updated_entry = food_repo.add_items_to_food_entry(user_id, entry_date, entry_id, new_items)
    
    if not updated_entry:
        return {"success": False, "message": "Entry not found.", "result": None}

    return {
        "success": True,
        "message": f"Added {len(new_items)} item(s) to entry.",
        "result": updated_entry
    }


def _handle_move_food_entry(data: Dict[str, Any], user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'move_food_entry': Change the meal category (e.g. from Lunch to Dinner).
    Data schema: { "entry_id": str, "meal": str }
    """
    entry_id = data.get("entry_id")
    new_meal = data.get("meal")

    if not entry_id or not new_meal:
         return {"success": False, "message": "Missing entry ID or target meal.", "result": None}

    # Update just the meal field
    updates = {"meal": new_meal}
    updated_entry = food_repo.update_food_entry(user_id, entry_date, entry_id, updates)

    if not updated_entry:
        return {"success": False, "message": "Entry not found.", "result": None}

    return {
        "success": True,
        "message": f"Moved entry to {new_meal}.",
        "result": updated_entry
    }


def _handle_delete_food_entry(data: Dict[str, Any], user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'delete_food_entry': Modify log to remove specific entry.
    Data schema: { "entry_id": str }
    """
    entry_id = data.get("entry_id")
    if not entry_id:
        return {"success": False, "message": "Missing entry ID to delete.", "result": None}

    success = food_repo.delete_food_entry(user_id, entry_date, entry_id)

    if success:
        return {"success": True, "message": "Entry deleted.", "result": {"entry_id": entry_id, "deleted": True}}
    else:
        return {"success": False, "message": "Could not delete entry (not found?).", "result": None}
