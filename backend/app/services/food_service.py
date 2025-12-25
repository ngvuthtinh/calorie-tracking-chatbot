from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.repositories import food_repo
from backend.app.services.nutrition_service import estimate_intake

class FoodService:
    """
    Service layer for Food operations. Encapsulates business logic and repo access.
    """
    
    @staticmethod
    def log_food(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log food items.
        """
        meal = data.get("meal", "snack")
        items = data.get("items", [])
        
        if not items:
             return {"success": False, "message": "No food items to log.", "result": None}

        entry_data = {
            "meal": meal,
            "items": items
        }

        try:
            # Create entry
            new_entry = food_repo.add_food_entry(user_id, entry_date, entry_data)

            # Calculate calories
            nutrition = estimate_intake(items)
            
            # Enrich result
            if new_entry:
                new_entry["nutrition"] = nutrition

            count = len(items)
            item_names = ", ".join([i.get("name", "food") for i in items])
            
            return {
                "success": True,
                "message": f"Logged {count} item(s) for {meal}: {item_names} ({nutrition['total_kcal']} kcal)",
                "result": new_entry
            }
        except Exception as e:
            # Log the actual error for debugging
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR in log_food: {error_details}")
            
            return {
                "success": False,
                "message": f"Failed to log food: {str(e)}",
                "result": None
            }

    @staticmethod
    def edit_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        if not entry_id:
             return {"success": False, "message": "Missing entry ID for edit.", "result": None}

        # Filter updates
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

    @staticmethod
    def add_food_items(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
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

    @staticmethod
    def move_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        new_meal = data.get("meal")

        if not entry_id or not new_meal:
             return {"success": False, "message": "Missing entry ID or target meal.", "result": None}

        updates = {"meal": new_meal}
        updated_entry = food_repo.update_food_entry(user_id, entry_date, entry_id, updates)

        if not updated_entry:
            return {"success": False, "message": "Entry not found.", "result": None}

        return {
            "success": True,
            "message": f"Moved entry to {new_meal}.",
            "result": updated_entry
        }

    @staticmethod
    def delete_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        if not entry_id:
            return {"success": False, "message": "Missing entry ID to delete.", "result": None}

        success = food_repo.delete_food_entry(user_id, entry_date, entry_id)

        if success:
            return {"success": True, "message": "Entry deleted.", "result": {"entry_id": entry_id, "deleted": True}}
        else:
            return {"success": False, "message": "Could not delete entry (not found?).", "result": None}
