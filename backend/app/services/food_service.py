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
            entry_code = new_entry.get('entry_code', f'f{new_entry["id"]}')
            meal_display = meal.capitalize()
            
            lines = [f"🍎 Logged {meal_display} ({entry_code}):"]
            for item in items_to_process:
                qty_display = f"{item.get('qty')} {item.get('unit', '')}".strip() if item.get('qty') else "1"
                lines.append(f"  • {qty_display} {item.get('name', 'item')} (+{item.get('kcal', 0)} kcal)")
            
            unknown_items = [b["name"] for b in nutrition["breakdown"] if b["status"] == "unknown"]
            if unknown_items:
                lines.append(f"\n⚠️  Could not find calories for: {', '.join(unknown_items)}")
            
            lines.append(f"\nTotal: +{nutrition['intake_kcal']} kcal")
            
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
             entry_code = data.get('entry_code', f'f{entry_id}')
             return {"success": False, "message": f"❌ Entry {entry_code} not found or could not be updated.", "result": None}

        # Build formatted message for Edit (if items were updated)
        entry_code = updated_entry.get('entry_code', f'f{entry_id}')
        if "items" in data:
            items_to_process = updates["items"]
            lines = [f"✏️ Updated {entry_code}:"]
            for item in items_to_process:
                qty_display = f"{item.get('qty')} {item.get('unit', '')}".strip() if item.get('qty') else "1"
                lines.append(f"  • {qty_display} {item.get('name', 'item')} (+{item.get('kcal', 0)} kcal)")
            lines.append(f"\nNew Total: {updates.get('intake_kcal', 0)} kcal")
            message = "\n".join(lines)
        else:
            message = f"✏️ Updated {entry_code} successfully."

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
        
        nutrition = estimate_intake(new_items)
        for i, breakdown in enumerate(nutrition["breakdown"]):
             if i < len(new_items):
                 new_items[i]["kcal"] = breakdown.get("kcal", 0)
                 new_items[i]["catalog_food_id"] = breakdown.get("catalog_id")

        updated_entry = food_repo.add_items_to_food_entry(user_id, entry_date, entry_id, new_items)
        
        if not updated_entry:
            return {"success": False, "message": f"❌ Entry [id:{entry_id}] not found.", "result": None}

        # Build formatted message
        entry_code = updated_entry.get('entry_code', f'f{entry_id}')
        meal_name = updated_entry.get('meal', 'Entry').capitalize()
        lines = [f"➕ Added to {meal_name} ({entry_code}):"]
        for item in new_items:
             qty_display = f"{item.get('qty')} {item.get('unit', '')}".strip() if item.get('qty') else "1"
             lines.append(f"  • {qty_display} {item.get('name', 'item')} (+{item.get('kcal', 0)} kcal)")
        
        lines.append(f"\nAdded: +{nutrition['intake_kcal']} kcal")
        
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
            return {"success": False, "message": f"❌ Entry {entry_id} not found.", "result": None}

        entry_code = updated_entry.get('entry_code', entry_id)
        return {
            "success": True,
            "message": f"➡️ Moved {entry_code} to {new_meal}.",
            "result": updated_entry
        }

    @staticmethod
    def delete_food_entry(user_id: int, entry_date: date, data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = data.get("entry_id")
        if not entry_id:
            return {"success": False, "message": "⚠️ Missing entry ID to delete.", "result": None}

        success = food_repo.delete_food_entry(user_id, entry_date, entry_id)

        if success:
            return {"success": True, "message": f"🗑️ Deleted {entry_id}.", "result": {"entry_id": entry_id, "deleted": True}}
        else:
            return {"success": False, "message": f"❌ Could not delete {entry_id}.", "result": None}
