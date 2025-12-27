from typing import Optional, List
from datetime import date
from backend.app.db.connection import fetch_one, execute, fetch_all

def get_day_session_id(user_id: int, entry_date: str) -> Optional[int]:
    """
    Get day_session_id for a user on a specific date. Returns None if not found.
    """
    query = "SELECT id FROM day_session WHERE user_id = %s AND entry_date = %s"
    row = fetch_one(query, (user_id, entry_date))
    
    if row:
        return row['id']
    return None

def get_or_create_day_session(user_id: int, entry_date: str) -> int:
    """
    Get day_session_id or create a new one if it doesn't exist.
    """
    existing_id = get_day_session_id(user_id, entry_date)
    if existing_id:
        return existing_id
    
    try:
        query_insert = "INSERT INTO day_session (user_id, entry_date) VALUES (%s, %s)"
        new_id = execute(query_insert, (user_id, entry_date))
        return new_id
    except Exception as e:
        # Likely a race condition (Duplicate entry), so check if it exists now
        existing_id = get_day_session_id(user_id, entry_date)
        if existing_id:
            return existing_id
        # Real error, re-raise
        raise e

def get_user_session_dates(user_id: int) -> List[date]:
    """
    Get all dates where the user logged something (has a day_session).
    Ordered by date DESC.
    """
    query = "SELECT entry_date FROM day_session WHERE user_id = %s ORDER BY entry_date DESC"
    rows = fetch_all(query, (user_id,))
    return [row['entry_date'] for row in rows]
