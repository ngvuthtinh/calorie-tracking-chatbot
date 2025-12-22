"""
Exercise Handlers Module

Handles all exercise-related intents:
- log_exercise
- edit_exercise_entry
- add_exercise_items
- delete_exercise_entry

All entries are stored scoped to the selected day in the context.
"""

from typing import Any, Dict, List, Optional
from datetime import date
from app.services.exercise_calorie_service import estimate_burn


def handle_exercise(intent: str, data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main router for exercise intents.
    
    Args:
        intent: The exercise intent name
        data: Parsed data from the semantic visitor
        repo: Repository access object (currently unused)
        context: Context dict containing user_id and date
        
    Returns:
        Dict with 'message' and optional 'result' keys
    """
    if intent == "log_exercise":
        return _handle_log_exercise(data, repo, context)
    elif intent == "edit_exercise_entry":
        return _handle_edit_exercise_entry(data, repo, context)
    elif intent == "edit_exercise_item":
        return _handle_edit_exercise_item(data, repo, context)
    elif intent == "add_exercise_items":
        return _handle_add_exercise_items(data, repo, context)
    elif intent == "delete_exercise_entry":
        return _handle_delete_exercise_entry(data, repo, context)
    else:
        return {"message": f"Unknown exercise intent: {intent}", "result": None}


def _validate_exercise_item(item: Dict[str, Any]) -> Optional[str]:
    """
    Validate that an exercise item has exactly ONE measurement type.
    
    Args:
        item: Exercise item dict
        
    Returns:
        Error message if validation fails, None if valid
    """
    measurements = []
    if "duration_min" in item and item["duration_min"] is not None:
        measurements.append("duration_min")
    if "distance_km" in item and item["distance_km"] is not None:
        measurements.append("distance_km")
    if "reps" in item and item["reps"] is not None:
        measurements.append("reps")
    
    if len(measurements) == 0:
        return f"Exercise item '{item.get('type', 'unknown')}' has no measurement (duration/distance/reps)"
    elif len(measurements) > 1:
        return f"Exercise item '{item.get('type', 'unknown')}' has multiple measurements: {', '.join(measurements)}. Only one is allowed."
    
    return None


def _generate_entry_id(context: Dict[str, Any]) -> str:
    """
    Generate a unique entry ID for exercise entries.
    Format: x<number> to match grammar pattern [xX][0-9]+
    """
    existing_entries = _get_exercise_entries(context)
    if not existing_entries:
        return "x1"
    
    # Extract numeric IDs and find the max
    max_id = 0
    for entry in existing_entries:
        entry_id = entry.get("entry_id", "")
        if entry_id.lower().startswith("x"):
            try:
                num = int(entry_id[1:])
                max_id = max(max_id, num)
            except ValueError:
                continue
    
    return f"x{max_id + 1}"


def _get_exercise_entries(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get or initialize the exercise_entries list in context."""
    if "exercise_entries" not in context:
        context["exercise_entries"] = []
    return context["exercise_entries"]


def _find_entry_by_id(entries: List[Dict[str, Any]], entry_id: str) -> Optional[Dict[str, Any]]:
    """Find an exercise entry by its ID."""
    for entry in entries:
        if entry.get("entry_id") == entry_id:
            return entry
    return None


def _handle_log_exercise(data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle log_exercise intent.
    
    Creates a new exercise entry with the provided items.
    
    Expected data format:
    {
        "items": [
            {"type": "run", "duration_min": 30},
            {"type": "pushups", "reps": 20}
        ]
    }
    """
    items = data.get("items", [])
    
    if not items:
        return {"message": "No exercise items provided", "result": None}
    
    # Validate all items
    for item in items:
        error = _validate_exercise_item(item)
        if error:
            return {"message": f"Validation error: {error}", "result": None}
    
    # Estimate calories burned
    profile = context.get("profile", {})
    calorie_estimate = estimate_burn(items, profile)
    
    # Create new entry
    entry_id = _generate_entry_id(context)
    entry = {
        "entry_id": entry_id,
        "items": items,
        "date": context.get("date"),
        "burned_kcal": calorie_estimate["burned_kcal"]
    }
    
    # Store in context
    entries = _get_exercise_entries(context)
    entries.append(entry)
    
    # Build response message
    item_descriptions = []
    for item in items:
        item_type = item.get("type", "unknown")
        if "duration_min" in item:
            item_descriptions.append(f"{item_type} {item['duration_min']}min")
        elif "distance_km" in item:
            item_descriptions.append(f"{item_type} {item['distance_km']}km")
        elif "reps" in item:
            item_descriptions.append(f"{item['reps']} {item_type}")
    
    message = f"Logged exercise [{entry_id}]: {', '.join(item_descriptions)} (~{calorie_estimate['burned_kcal']} kcal burned)"
    
    return {
        "message": message,
        "result": {
            "entry_id": entry_id,
            "items": items,
            "burned_kcal": calorie_estimate["burned_kcal"],
            "breakdown": calorie_estimate["breakdown"]
        }
    }


def _handle_edit_exercise_entry(data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle edit_exercise_entry intent.
    
    Replaces an existing exercise entry with new items.
    
    Expected data format:
    {
        "entry_id": "ex_001",
        "items": [
            {"type": "run", "duration_min": 45}
        ]
    }
    """
    entry_id = data.get("entry_id")
    items = data.get("items", [])
    
    if not entry_id:
        return {"message": "No entry_id provided", "result": None}
    
    if not items:
        return {"message": "No exercise items provided", "result": None}
    
    # Validate all items
    for item in items:
        error = _validate_exercise_item(item)
        if error:
            return {"message": f"Validation error: {error}", "result": None}
    
    # Find existing entry
    entries = _get_exercise_entries(context)
    entry = _find_entry_by_id(entries, entry_id)
    
    if not entry:
        return {"message": f"Exercise entry '{entry_id}' not found", "result": None}
    
    # Update entry
    entry["items"] = items
    
    # Build response message
    item_descriptions = []
    for item in items:
        item_type = item.get("type", "unknown")
        if "duration_min" in item:
            item_descriptions.append(f"{item_type} {item['duration_min']}min")
        elif "distance_km" in item:
            item_descriptions.append(f"{item_type} {item['distance_km']}km")
        elif "reps" in item:
            item_descriptions.append(f"{item['reps']} {item_type}")
    
    message = f"Updated exercise [{entry_id}]: {', '.join(item_descriptions)}"
    
    return {
        "message": message,
        "result": {
            "entry_id": entry_id,
            "items": items
        }
    }


def _handle_edit_exercise_item(data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle edit_exercise_item intent.
    
    Edits a specific item within an existing exercise entry by index.
    
    Expected data format:
    {
        "entry_id": "x1",
        "item_index": 1,
        "item": {"type": "run", "duration_min": 45}
    }
    """
    entry_id = data.get("entry_id")
    item_index = data.get("item_index")
    item = data.get("item")
    
    if not entry_id:
        return {"message": "No entry_id provided", "result": None}
    
    if item_index is None:
        return {"message": "No item_index provided", "result": None}
    
    if not item:
        return {"message": "No exercise item provided", "result": None}
    
    # Validate the new item
    error = _validate_exercise_item(item)
    if error:
        return {"message": f"Validation error: {error}", "result": None}
    
    # Find existing entry
    entries = _get_exercise_entries(context)
    entry = _find_entry_by_id(entries, entry_id)
    
    if not entry:
        return {"message": f"Exercise entry '{entry_id}' not found", "result": None}
    
    # Validate item index (1-indexed from user, convert to 0-indexed)
    items_list = entry.get("items", [])
    if item_index < 1 or item_index > len(items_list):
        return {
            "message": f"Invalid item index {item_index}. Entry '{entry_id}' has {len(items_list)} item(s)",
            "result": None
        }
    
    # Replace the specific item (convert to 0-indexed)
    array_index = item_index - 1
    old_item = items_list[array_index]
    items_list[array_index] = item
    
    # Build response message
    item_type = item.get("type", "unknown")
    if "duration_min" in item:
        new_desc = f"{item_type} {item['duration_min']}min"
    elif "distance_km" in item:
        new_desc = f"{item_type} {item['distance_km']}km"
    elif "reps" in item:
        new_desc = f"{item['reps']} {item_type}"
    else:
        new_desc = str(item)
    
    message = f"Updated item {item_index} in exercise [{entry_id}]: {new_desc}"
    
    return {
        "message": message,
        "result": {
            "entry_id": entry_id,
            "item_index": item_index,
            "old_item": old_item,
            "new_item": item
        }
    }


def _handle_add_exercise_items(data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle add_exercise_items intent.
    
    Adds new items to an existing exercise entry.
    
    Expected data format:
    {
        "entry_id": "ex_001",
        "items": [
            {"type": "squats", "reps": 30}
        ]
    }
    """
    entry_id = data.get("entry_id")
    items = data.get("items", [])
    
    if not entry_id:
        return {"message": "No entry_id provided", "result": None}
    
    if not items:
        return {"message": "No exercise items provided", "result": None}
    
    # Validate all items
    for item in items:
        error = _validate_exercise_item(item)
        if error:
            return {"message": f"Validation error: {error}", "result": None}
    
    # Find existing entry
    entries = _get_exercise_entries(context)
    entry = _find_entry_by_id(entries, entry_id)
    
    if not entry:
        return {"message": f"Exercise entry '{entry_id}' not found", "result": None}
    
    # Add items to entry
    entry["items"].extend(items)
    
    # Build response message
    item_descriptions = []
    for item in items:
        item_type = item.get("type", "unknown")
        if "duration_min" in item:
            item_descriptions.append(f"{item_type} {item['duration_min']}min")
        elif "distance_km" in item:
            item_descriptions.append(f"{item_type} {item['distance_km']}km")
        elif "reps" in item:
            item_descriptions.append(f"{item['reps']} {item_type}")
    
    message = f"Added to exercise [{entry_id}]: {', '.join(item_descriptions)}"
    
    return {
        "message": message,
        "result": {
            "entry_id": entry_id,
            "added_items": items,
            "total_items": len(entry["items"])
        }
    }


def _handle_delete_exercise_entry(data: Dict[str, Any], repo: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle delete_exercise_entry intent.
    
    Deletes an exercise entry by ID.
    
    Expected data format:
    {
        "entry_id": "ex_001"
    }
    """
    entry_id = data.get("entry_id")
    
    if not entry_id:
        return {"message": "No entry_id provided", "result": None}
    
    # Find and remove entry
    entries = _get_exercise_entries(context)
    entry = _find_entry_by_id(entries, entry_id)
    
    if not entry:
        return {"message": f"Exercise entry '{entry_id}' not found", "result": None}
    
    entries.remove(entry)
    
    message = f"Deleted exercise entry [{entry_id}]"
    
    return {
        "message": message,
        "result": {
            "entry_id": entry_id,
            "deleted": True
        }
    }
