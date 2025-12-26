from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.repositories import exercise_repo, action_log_repo
from backend.app.services.exercise_calorie_service import estimate_burn

class ExerciseService:
    """
    Service layer for Exercise operations. Encapsulates business logic and repo access.
    """

    @staticmethod
    def _validate_exercise_item(item: Dict[str, Any]) -> Optional[str]:
        """
        Validate that an exercise item has exactly ONE measurement type.
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

    @classmethod
    def log_exercise(cls, user_id: int, entry_date: date, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        items = data.get("items", [])
        
        if not items:
            return {"success": False, "message": "No exercise items provided", "result": None}
        
        # Validate all items
        for item in items:
            error = cls._validate_exercise_item(item)
            if error:
                return {"success": False, "message": f"Validation error: {error}", "result": None}
        
        # Estimate calories burned
        profile = context.get("profile", {})
        calorie_estimate = estimate_burn(items, profile)
        
        # Prepare entry structure
        entry = {
            "items": items,
            "burned_kcal": calorie_estimate["burned_kcal"]
        }
        
        # Save to database
        new_entry = exercise_repo.add_exercise_entry(user_id, entry_date, entry)
        
        # Log action
        action_log_repo.log_action(
            day_session_id=new_entry["day_session_id"],
            action_type="create_exercise",
            ref_table="exercise_entry",
            ref_id=new_entry["id"]
        )
        
        # Add calorie info to result (repo already adds it, but we can ensure structure)
        new_entry["breakdown"] = calorie_estimate["breakdown"]
        
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
        
        message = f"Logged exercise [{new_entry['entry_code']}]: {', '.join(item_descriptions)} (~{calorie_estimate['burned_kcal']} kcal burned)"
        
        return {
            "success": True,
            "message": message,
            "result": new_entry
        }

    @classmethod
    def edit_exercise_entry(cls, user_id: int, entry_date: date, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        items = data.get("items", [])
        
        if not entry_id:
            return {"success": False, "message": "No entry_id provided", "result": None}
        
        if not items:
            return {"success": False, "message": "No exercise items provided", "result": None}
        
        # Validate all items
        for item in items:
            error = cls._validate_exercise_item(item)
            if error:
                return {"success": False, "message": f"Validation error: {error}", "result": None}
        

        
        updated_entry = exercise_repo.update_exercise_entry(user_id, entry_date, entry_id, {"items": items})
        
        if not updated_entry:
             return {"success": False, "message": "Entry not found or could not be updated.", "result": None}
        
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
            "success": True,
            "message": message,
            "result": {
                "entry_id": entry_id,
                "items": items
            }
        }

    @classmethod
    def edit_exercise_item(cls, user_id: int, entry_date: date, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        item_index = data.get("item_index")
        item = data.get("item")
        
        if not entry_id:
            return {"success": False, "message": "No entry_id provided", "result": None}
        if item_index is None:
            return {"success": False, "message": "No item_index provided", "result": None}
        if not item:
            return {"success": False, "message": "No exercise item provided", "result": None}
        
        error = cls._validate_exercise_item(item)
        if error:
            return {"success": False, "message": f"Validation error: {error}", "result": None}


        
        entry = exercise_repo.get_exercise_entry(user_id, entry_date, entry_id)
        if not entry:
             return {"success": False, "message": f"Exercise entry '{entry_id}' not found", "result": None}

        items_list = entry.get("items", [])
        if item_index < 1 or item_index > len(items_list):
            return {
                "success": False,
                "message": f"Invalid item index {item_index}. Entry '{entry_id}' has {len(items_list)} item(s)",
                "result": None
            }
            
        array_index = item_index - 1
        old_item = items_list[array_index]
        items_list[array_index] = item
        
        updated_entry = exercise_repo.update_exercise_entry(user_id, entry_date, entry_id, {"items": items_list})
        
        # Response construction...
        item_type = item.get("type", "unknown")
        # ... (simplified for brevity, can copy logic)
        new_desc = item_type # Placeholder
        
        return {
            "success": True,
            "message": f"Updated item {item_index} in exercise [{entry_id}]",
            "result": {
                "entry_id": entry_id,
                "item_index": item_index,
                "old_item": old_item,
                "new_item": item
            }
        }

    @classmethod
    def add_exercise_items(cls, user_id: int, entry_date: date, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        items = data.get("items", [])
        
        if not entry_id or not items:
            return {"success": False, "message": "Missing info", "result": None}
            
        for item in items:
            error = cls._validate_exercise_item(item)
            if error: return {"success": False, "message": error}
            
        updated_entry = exercise_repo.add_items_to_exercise_entry(user_id, entry_date, entry_id, items)
        
        if not updated_entry:
             return {"success": False, "message": "Entry not found.", "result": None}
             
        return {
            "success": True, 
            "message": f"Added {len(items)} items.", 
            "result": updated_entry
        }

    @classmethod
    def delete_exercise_entry(cls, user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        if not entry_id:
             return {"success": False, "message": "Missing ID", "result": None}
             
        success = exercise_repo.delete_exercise_entry(user_id, entry_date, entry_id)
        
        if success:
            return {"success": True, "message": "Deleted.", "result": {"deleted": True}}
        return {"success": False, "message": "Failed to delete.", "result": None}
