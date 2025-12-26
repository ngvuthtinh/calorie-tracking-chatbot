from datetime import date
from typing import Optional
from backend.app.db.connection import execute

def log_action(day_session_id: int, action_type: str, ref_table: str, ref_id: int) -> int:
    """
    Log a user action into action_log table.
    
    Args:
        day_session_id: ID of the day_session
        action_type: Type of action (e.g. 'create_food', 'edit_food', 'delete_food')
        ref_table: Table name of the affected entity (e.g. 'food_entry')
        ref_id: ID of the affected entity
        
    Returns:
        ID of the inserted log entry
    """
    query = """
        INSERT INTO action_log (day_session_id, action_type, ref_table, ref_id, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """
    
    return execute(query, (day_session_id, action_type, ref_table, ref_id))
