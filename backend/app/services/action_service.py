from typing import Dict, Any, Optional
from backend.app.repositories import action_log_repo, food_repo, exercise_repo

class ActionService:
    @staticmethod
    def undo_last_action(user_id: int, date_str: str, scope: Optional[str] = None) -> Dict[str, Any]:
        """
        Undo the last action for a user on a given date.
        Optionally scoped to 'food' or 'exercise'.
        """
        # Determine table filter
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
            return {"success": False, "message": f"Cannot undo action of type '{action_type}'.", "result": None}
            
        # Remove the log entry
        action_log_repo.delete_log(last_action["id"])
        
        return {
            "success": True, 
            "message": f"Undid last action: {undone_item}.", 
            "result": {"undone_action": action_type, "ref_id": ref_id}
        }
