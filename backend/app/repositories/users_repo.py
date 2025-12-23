from typing import Optional
from backend.app.db.connection import fetch_one, execute

def get_or_create_user(email: str) -> int:
    """
    Get user ID by email. If user does not exist, create a new one.
    """
    query_check = "SELECT id FROM users WHERE email = %s"
    row = fetch_one(query_check, (email,))
    
    if row:
        return row['id']
    
    query_insert = "INSERT INTO users (email) VALUES (%s)"
    new_id = execute(query_insert, (email,))
    return new_id
