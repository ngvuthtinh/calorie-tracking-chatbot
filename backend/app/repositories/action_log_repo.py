from datetime import date
from typing import Optional, Dict, Any, List
from backend.app.db.connection import execute, fetch_one, fetch_all

def log_action(day_session_id: int, action_type: str, ref_table: str, ref_id: int) -> int:
    """
    Log a user action into action_log table.
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

def get_user_logs(user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get recent logs for a user (useful for overview/debug).
    """
    query = """
        SELECT al.id, al.action_type, al.created_at
        FROM action_log al
        JOIN day_session ds ON al.day_session_id = ds.id
        WHERE ds.user_id = %s
        ORDER BY al.created_at DESC
        LIMIT %s
    """
    return fetch_all(query, (user_id, limit))
