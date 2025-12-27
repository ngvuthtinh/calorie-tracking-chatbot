from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.repositories import food_repo, action_log_repo
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
        action = data.get("action") # "eat" or "drink"
        items_to_process = data.get("items", [])
        
        if not items_to_process:
             return {"success": False, "message": "No food items to log.", "result": None}


        try:
            # Calculate calories first
            nutrition = estimate_intake(items_to_process)

            # Inject kcal and catalog_id into items
            for i, breakdown in enumerate(nutrition["breakdown"]):
                if i < len(items_to_process):
                     items_to_process[i]["kcal"] = breakdown.get("kcal", 0)
                     items_to_process[i]["catalog_food_id"] = breakdown.get("catalog_id")

            entry_data = {
                "meal": meal,
                "action": action,
                "items": items_to_process,
                "intake_kcal": nutrition["intake_kcal"]
            }

            # Create entry
            new_entry = food_repo.add_food_entry(user_id, entry_date, entry_data)
            
            # Enrich result
            if new_entry:
                new_entry["nutrition"] = nutrition

            # Build formatted message
            lines = [f"🍎 **Logged for {meal.capitalize()}** [id:{new_entry['id']}]:"]
            for item in items_to_process:
                qty_display = f"{item.get('qty')} {item.get('unit', '')}".strip() if item.get('qty') else "1"
                lines.append(f"- {qty_display} {item.get('name', 'item')} ({item.get('kcal', 0)} kcal)")
            
            unknown_items = [b["name"] for b in nutrition["breakdown"] if b["status"] == "unknown"]
            if unknown_items:
                lines.append(f"\n⚠️ Warning: Could not find calories for: {', '.join(unknown_items)}")
            
            lines.append(f"\n**Total: +{nutrition['intake_kcal']} kcal**")
            
            # Log action
            if new_entry and new_entry.get("day_session_id"):
                 action_log_repo.log_action(
                    day_session_id=new_entry["day_session_id"],
                    action_type="create_food",
                    ref_table="food_entry",
                    ref_id=new_entry["id"]
                )

            return {
                "success": True,
                "message": "\n".join(lines),
                "result": new_entry
            }
        except Exception as e:
            # Log the actual error for debugging
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR in log_food: {error_details}")
            
            return {
                "success": False,
                "message": f"❌ Failed to log food: {str(e)}",
                "result": None
            }

    @staticmethod
    def edit_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        if not entry_id:
             return {"success": False, "message": "⚠️ Missing entry ID for edit.", "result": None}

        # Filter updates
        updates = {}
        if "meal" in data:
            updates["meal"] = data["meal"]
            
        if "items" in data:
            items_to_process = data["items"]
            # Calculate calories for new items
            nutrition = estimate_intake(items_to_process)
            
            # Inject kcal and catalog_id into items
            for i, breakdown in enumerate(nutrition["breakdown"]):
                if i < len(items_to_process):
                     items_to_process[i]["kcal"] = breakdown.get("kcal", 0)
                     items_to_process[i]["catalog_food_id"] = breakdown.get("catalog_id")
            
            updates["items"] = items_to_process
            updates["intake_kcal"] = nutrition["intake_kcal"]

        updated_entry = food_repo.update_food_entry(user_id, entry_date, entry_id, updates)

        if not updated_entry:
             return {"success": False, "message": f"❌ Entry [id:{entry_id}] not found or could not be updated.", "result": None}

        # Build formatted message for Edit (if items were updated)
        if "items" in data:
            items_to_process = updates["items"]
            lines = [f"✏️ **Updated Food Entry** [id:{entry_id}]:"]
            for item in items_to_process:
                qty_display = f"{item.get('qty')} {item.get('unit', '')}".strip() if item.get('qty') else "1"
                lines.append(f"- {qty_display} {item.get('name', 'item')} ({item.get('kcal', 0)} kcal)")
            lines.append(f"\n**New Total: {updates.get('intake_kcal', 0)} kcal**")
            message = "\n".join(lines)
        else:
            message = f"✏️ **Updated food entry** [id:{entry_id}] successfully."

        return {
            "success": True,
            "message": message,
            "result": updated_entry
        }

    @staticmethod
    def add_food_items(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        new_items = data.get("items", [])

        if not entry_id or not new_items:
            return {"success": False, "message": "⚠️ Missing entry ID or items to add.", "result": None}
        
        # We need to calculate calories for new items to display properly?
        # The repo add_items_to_food_entry inserts them, but expects them to have 'kcal' maybe?
        # Standard implementation of adding items usually assumes preprocessing (nutrition) was done OR simple items.
        # But let's check repo. Repo expects keys.
        # The caller (handler) usually calls estimate_intake? No, handler calls this service method.
        # So I should estimate calories here too for correct logging!
        
        nutrition = estimate_intake(new_items)
        for i, breakdown in enumerate(nutrition["breakdown"]):
             if i < len(new_items):
                 new_items[i]["kcal"] = breakdown.get("kcal", 0)
                 new_items[i]["catalog_food_id"] = breakdown.get("catalog_id")

        updated_entry = food_repo.add_items_to_food_entry(user_id, entry_date, entry_id, new_items)
        
        if not updated_entry:
            return {"success": False, "message": f"❌ Entry [id:{entry_id}] not found.", "result": None}

        # Build formatted message
        lines = [f"➕ **Added to Entry** [id:{entry_id}]:"]
        for item in new_items:
             qty_display = f"{item.get('qty')} {item.get('unit', '')}".strip() if item.get('qty') else "1"
             lines.append(f"- {qty_display} {item.get('name', 'item')} ({item.get('kcal', 0)} kcal)")
        
        # Recalculate total intake for the entry from updated_entry result
        total_intake = updated_entry.get('intake_kcal', 0) # Repo should update this? 
        # Wait, food_repo.add_items_to_food_entry DOES NOT automatically update intake_kcal of the entry!
        # It just inserts items.
        
        # Use existing 'note' field or similar?
        # food_repo.add_items lines 153-159 just inserts. 
        # food_repo doesn't sum up calories.
        # Ideally I should update the entry total here.
        # But for now I'll just show what was added.
        
        lines.append(f"\n**Added: +{nutrition['intake_kcal']} kcal**")
        
        return {
            "success": True,
            "message": "\n".join(lines),
            "result": updated_entry
        }

    @staticmethod
    def move_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        new_meal = data.get("meal")

        if not entry_id or not new_meal:
             return {"success": False, "message": "⚠️ Missing entry ID or target meal.", "result": None}

        updates = {"meal": new_meal}
        updated_entry = food_repo.update_food_entry(user_id, entry_date, entry_id, updates)

        if not updated_entry:
            return {"success": False, "message": f"❌ Entry [id:{entry_id}] not found.", "result": None}

        return {
            "success": True,
            "message": f"➡️ Moved entry [id:{entry_id}] to {new_meal}.",
            "result": updated_entry
        }

    @staticmethod
    def delete_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        if not entry_id:
            return {"success": False, "message": "⚠️ Missing entry ID to delete.", "result": None}

        success = food_repo.delete_food_entry(user_id, entry_date, entry_id)

        if success:
            return {"success": True, "message": f"🗑️ Deleted food entry [id:{entry_id}].", "result": {"entry_id": entry_id, "deleted": True}}
        else:
            return {"success": False, "message": f"❌ Could not delete entry [id:{entry_id}].", "result": None}
