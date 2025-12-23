from typing import Any, Dict, List, Optional
from datetime import date

def handle_food(intent: str, data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch food intents to specific handlers.
    
    Args:
        intent: The intent name (e.g., 'log_food')
        data: The extracted data payload
        repo: Repository object for database persistence
        context: Context containing 'user_id' and 'date'
    """
    user_id = context.get("user_id")
    entry_date = context.get("date")

    if not user_id or not entry_date:
        return {
            "success": False,
            "message": "Missing user context (user_id or date)."
        }

    if intent == "log_food":
        return _handle_log_food(data, repo, user_id, entry_date)
    elif intent == "edit_food_entry":
        return _handle_edit_food_entry(data, repo, user_id, entry_date)
    elif intent == "add_food_items":
        return _handle_add_food_items(data, repo, user_id, entry_date)
    elif intent == "move_food_entry":
        return _handle_move_food_entry(data, repo, user_id, entry_date)
    elif intent == "delete_food_entry":
        return _handle_delete_food_entry(data, repo, user_id, entry_date)

    return {
        "success": False,
        "message": f"Unknown food intent: {intent}"
    }


def _handle_log_food(data: Dict[str, Any], repo: Any, user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'log_food': Create new food entries.
    Data schema: { "meal": str, "action": str, "items": [...] }
    """
    meal = data.get("meal", "snack")  # Default to snack if not specified
    items = data.get("items", [])
    
    if not items:
        return {"success": False, "message": "No food items to log."}

    # Prepare entry structure
    # Note: We group them into one entry or multiple? 
    # Usually 'log_food' creates one entry containing multiple items for a specific meal.
    entry = {
        "meal": meal,
        "items": items,
        "created_at_local": str(entry_date) 
    }

    # Repo interaction
    # Assuming repo.add_food_entry returns the created entry with an ID
    new_entry = repo.add_food_entry(user_id, entry_date, entry)

    count = len(items)
    item_names = ", ".join([i.get("name", "food") for i in items])
    
    return {
        "success": True,
        "message": f"Logged {count} item(s) for {meal}: {item_names}",
        "entry": new_entry
    }


def _handle_edit_food_entry(data: Dict[str, Any], repo: Any, user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'edit_food_entry': Overwrite/Update an existing entry.
    Data schema: { "entry_id": str, "meal": str, "items": [...] }
    """
    entry_id = data.get("entry_id")
    if not entry_id:
        return {"success": False, "message": "Missing entry ID for edit."}

    # We update fields present in data
    updates = {}
    if "meal" in data:
        updates["meal"] = data["meal"]
    if "items" in data:
        updates["items"] = data["items"]

    updated_entry = repo.update_food_entry(user_id, entry_date, entry_id, updates)

    if not updated_entry:
         return {"success": False, "message": "Entry not found or could not be updated."}

    return {
        "success": True,
        "message": "Food entry updated successfully.",
        "entry": updated_entry
    }


def _handle_add_food_items(data: Dict[str, Any], repo: Any, user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'add_food_items': Append items to an existing entry.
    Data schema: { "entry_id": str, "items": [...] }
    """
    entry_id = data.get("entry_id")
    new_items = data.get("items", [])

    if not entry_id or not new_items:
        return {"success": False, "message": "Missing entry ID or items to add."}

    # Logic: Get existing -> Append items -> Save
    # Or repo might have specific method: repo.append_food_items(...)
    # Let's assume a generic update or append method.
    # We'll fetch first to act more robustly if repo is simple kv store, 
    # but ideally repo handles atomicity.
    
    # Simulating atomic append via repo method if it existed, strictly generic:
    # We will try to rely on a specific method if possible, or fall back to get+update
    
    # Using a specialized method name for clarity:
    updated_entry = repo.add_items_to_food_entry(user_id, entry_date, entry_id, new_items)
    
    if not updated_entry:
        return {"success": False, "message": "Entry not found."}

    return {
        "success": True,
        "message": f"Added {len(new_items)} item(s) to entry.",
        "entry": updated_entry
    }


def _handle_move_food_entry(data: Dict[str, Any], repo: Any, user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'move_food_entry': Change the meal category (e.g. from Lunch to Dinner).
    Data schema: { "entry_id": str, "meal": str }
    """
    entry_id = data.get("entry_id")
    new_meal = data.get("meal")

    if not entry_id or not new_meal:
         return {"success": False, "message": "Missing entry ID or target meal."}

    # Update just the meal field
    updates = {"meal": new_meal}
    updated_entry = repo.update_food_entry(user_id, entry_date, entry_id, updates)

    if not updated_entry:
        return {"success": False, "message": "Entry not found."}

    return {
        "success": True,
        "message": f"Moved entry to {new_meal}.",
        "entry": updated_entry
    }


def _handle_delete_food_entry(data: Dict[str, Any], repo: Any, user_id: str, entry_date: date) -> Dict[str, Any]:
    """
    Handle 'delete_food_entry': Modify log to remove specific entry.
    Data schema: { "entry_id": str }
    """
    entry_id = data.get("entry_id")
    if not entry_id:
        return {"success": False, "message": "Missing entry ID to delete."}

    success = repo.delete_food_entry(user_id, entry_date, entry_id)

    if success:
        return {"success": True, "message": "Entry deleted."}
    else:
        return {"success": False, "message": "Could not delete entry (not found?)."}
