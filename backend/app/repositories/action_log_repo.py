from datetime import date
from typing import Optional, Dict, Any
from backend.app.db.connection import execute, fetch_one

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

def get_last_action(user_id: int, date_str: str, table_filter: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get the last logged action for a user on a specific date.
    Optionally filter by table name (e.g. 'food_entry').
    """
    query = """
        SELECT al.id, al.action_type, al.ref_table, al.ref_id, al.created_at
        FROM action_log al
        JOIN day_session ds ON al.day_session_id = ds.id
        WHERE ds.user_id = %s AND ds.entry_date = %s
    """
    params = [user_id, date_str]
    
    if table_filter:
        query += " AND al.ref_table = %s"
        params.append(table_filter)
        
    query += " ORDER BY al.created_at DESC LIMIT 1"
    
    return fetch_one(query, tuple(params))

def delete_log(log_id: int) -> None:
    """
    Delete a log entry by ID.
    """
    execute("DELETE FROM action_log WHERE id = %s", (log_id,))

