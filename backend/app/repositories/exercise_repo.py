from typing import Any, Dict, List, Optional
from datetime import date
from backend.app.db.connection import execute, fetch_one, fetch_all
from backend.app.repositories.day_session_repo import get_or_create_day_session

def add_exercise_entry(user_id: int, entry_date: date, entry_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new exercise entry for the given user and date.
    entry_data: { "items": [{ "type": str, "duration_min": ..., "distance_km": ..., "reps": ... }] }
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    # Generate entry_code (e.g., x1, x2)
    count_query = "SELECT COUNT(*) as c FROM exercise_entry WHERE day_session_id = %s"
    row = fetch_one(count_query, (session_id,))
    count = row['c'] if row else 0
    entry_code = f"x{count + 1}"
    
    # Insert exercise_entry
    query_entry = """
        INSERT INTO exercise_entry (day_session_id, entry_code, burned_kcal, created_at)
        VALUES (%s, %s, %s, NOW())
    """
    burned_kcal = entry_data.get('burned_kcal', 0)
    entry_db_id = execute(query_entry, (session_id, entry_code, burned_kcal))
    
    # Insert items
    items = entry_data.get('items', [])
    saved_items = []
    for item in items:
        query_item = """
            INSERT INTO exercise_item (exercise_entry_id, ex_type, duration_min, distance_km, reps, note)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute(query_item, (
            entry_db_id,
            item.get('type'),
            item.get('duration_min'),
            item.get('distance_km'),
            item.get('reps'),
            item.get('note')
        ))
        saved_items.append(item)
        
    return {
        "id": entry_db_id,
        "day_session_id": session_id,
        "entry_code": entry_code,
        "burned_kcal": burned_kcal,
        "items": saved_items,
        "created_at_local": str(entry_date)
    }

def update_exercise_entry(user_id: int, entry_date: date, entry_code: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Updates an existing exercise entry identified by entry_code.
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    query_find = "SELECT id FROM exercise_entry WHERE day_session_id = %s AND entry_code = %s AND is_deleted = FALSE"
    row = fetch_one(query_find, (session_id, entry_code))
    if not row:
        return None
    
    entry_db_id = row['id']
    
    if 'items' in updates or 'burned_kcal' in updates:
        if 'burned_kcal' in updates:
             execute("UPDATE exercise_entry SET burned_kcal = %s WHERE id = %s", (updates['burned_kcal'], entry_db_id))

        if 'items' in updates:
            execute("DELETE FROM exercise_item WHERE exercise_entry_id = %s", (entry_db_id,))
            for item in updates['items']:
                query_item = """
                    INSERT INTO exercise_item (exercise_entry_id, ex_type, duration_min, distance_km, reps, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                execute(query_item, (
                    entry_db_id,
                    item.get('type'),
                    item.get('duration_min'),
                    item.get('distance_km'),
                    item.get('reps'),
                    item.get('note')
                ))

    return _get_exercise_entry_details(entry_db_id)

def add_items_to_exercise_entry(user_id: int, entry_date: date, entry_code: str, new_items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Appends items to an existing exercise entry.
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    query_find = "SELECT id FROM exercise_entry WHERE day_session_id = %s AND entry_code = %s AND is_deleted = FALSE"
    row = fetch_one(query_find, (session_id, entry_code))
    if not row:
        return None
        
    entry_db_id = row['id']
    
    for item in new_items:
        query_item = """
            INSERT INTO exercise_item (exercise_entry_id, ex_type, duration_min, distance_km, reps, note)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute(query_item, (
            entry_db_id,
            item.get('type'),
            item.get('duration_min'),
            item.get('distance_km'),
            item.get('reps'),
            item.get('note')
        ))
            
    return _get_exercise_entry_details(entry_db_id)

def delete_exercise_entry(user_id: int, entry_date: date, entry_code: str) -> bool:
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    query_find = "SELECT id FROM exercise_entry WHERE day_session_id = %s AND entry_code = %s"
    row = fetch_one(query_find, (session_id, entry_code))
    if not row:
        return False
        
    entry_db_id = row['id']
    execute("UPDATE exercise_entry SET is_deleted = TRUE WHERE id = %s", (entry_db_id,))
    return True

def list_exercise_entries(user_id: int, entry_date: date) -> List[Dict[str, Any]]:
    """
    List all exercise entries for a given user and date.
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    if not session_id:
        return []
        
    # Get all non-deleted entries for this day
    query = """
        SELECT id, entry_code, created_at
        FROM exercise_entry
        WHERE day_session_id = %s AND is_deleted = FALSE
        ORDER BY created_at ASC
    """
    entries = fetch_all(query, (session_id,))
    
    # Get details for each entry
    result = []
    for entry_row in entries:
        entry_details = _get_exercise_entry_details(entry_row['id'])
        result.append(entry_details)
    
    return result

# Alias for StatsService compatibility
def get_day_exercise_entries(user_id: int, entry_date: date) -> List[Dict[str, Any]]:
    return list_exercise_entries(user_id, entry_date)

def get_exercise_entries_in_range(user_id: int, start_date: date, end_date: date) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all exercise entries within range.
    """
    query = """
        SELECT ds.entry_date, ee.id, ee.burned_kcal
        FROM day_session ds
        JOIN exercise_entry ee ON ee.day_session_id = ds.id
        WHERE ds.user_id = %s AND ds.entry_date >= %s AND ds.entry_date <= %s AND ee.is_deleted = FALSE
    """
    rows = fetch_all(query, (user_id, start_date, end_date))
    
    by_date = {}
    for r in rows:
        d_str = str(r['entry_date'])
        if d_str not in by_date:
            by_date[d_str] = []
        
        by_date[d_str].append({
            "burned_kcal": float(r['burned_kcal'])
        })
    return by_date

def get_exercise_entry(user_id: int, entry_date: date, entry_code: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific exercise entry by code.
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    query = "SELECT id FROM exercise_entry WHERE day_session_id = %s AND entry_code = %s AND is_deleted = FALSE"
    row = fetch_one(query, (session_id, entry_code))
    if not row:
        return None
    return _get_exercise_entry_details(row['id'])

def _get_exercise_entry_details(entry_db_id: int) -> Dict[str, Any]:
    query_entry = "SELECT * FROM exercise_entry WHERE id = %s"
    entry_row = fetch_one(query_entry, (entry_db_id,))
    if not entry_row:
        return {}
        
    query_items = "SELECT * FROM exercise_item WHERE exercise_entry_id = %s"
    items_rows = fetch_all(query_items, (entry_db_id,))
    
    items = []
    for ir in items_rows:
        item = {
            "type": ir['ex_type']
        }
        if ir.get('duration_min'):
            item['duration_min'] = int(ir['duration_min'])
        if ir.get('distance_km'):
            item['distance_km'] = float(ir['distance_km'])
        if ir.get('reps'):
            item['reps'] = int(ir['reps'])
        if ir.get('note'):
            item['note'] = ir['note']
        items.append(item)
        
    return {
        "id": entry_row['id'],
        "day_session_id": entry_row['day_session_id'],
        "entry_code": entry_row['entry_code'],
        "burned_kcal": float(entry_row['burned_kcal']) if entry_row['burned_kcal'] else 0.0,
        "items": items,
        "created_at_local": str(entry_row['created_at'])
    }

def delete_exercise_entry_by_id(entry_id: int) -> bool:
    """
    Soft delete an exercise entry by its DB ID.
    """
    execute("UPDATE exercise_entry SET is_deleted = TRUE WHERE id = %s", (entry_id,))
    return True
