from typing import Any, Dict, List, Optional
from datetime import date, datetime
from backend.app.db.connection import execute, fetch_one, fetch_all
from backend.app.repositories.day_session_repo import get_or_create_day_session, get_day_session_id

def add_food_entry(user_id: int, entry_date: date, entry_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new food entry for the given user and date.
    entry_data: { "meal": str, "items": [{ "name": str, "qty": ..., "unit": ... }] }
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    # Generate entry_code (e.g., f1, f2)
    count_query = "SELECT COUNT(*) as c FROM food_entry WHERE day_session_id = %s"
    row = fetch_one(count_query, (session_id,))
    count = row['c'] if row else 0
    entry_code = f"f{count + 1}"
    
    # Insert food_entry
    query_entry = """
        INSERT INTO food_entry (day_session_id, entry_code, meal, action, intake_kcal, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    meal = entry_data.get('meal', 'snack')
    action = entry_data.get('action') # "eat" or "drink"
    intake_kcal = entry_data.get('intake_kcal', 0)
    entry_db_id = execute(query_entry, (session_id, entry_code, meal, action, intake_kcal))
    
    # Insert items
    items = entry_data.get('items', [])
    saved_items = []
    for item in items:
        query_item = """
            INSERT INTO food_item (food_entry_id, item_name, qty, unit, kcal, note)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        qty = item.get('qty')
        if qty == 'UNKNOWN': 
            qty = None
        
        kcal = item.get('kcal', 0)
        execute(query_item, (entry_db_id, item.get('name'), qty, item.get('unit'), kcal, item.get('note')))
        saved_items.append(item)
        
    return {
        "id": entry_db_id,
        "day_session_id": session_id,
        "entry_code": entry_code,
        "meal": meal,
        "action": action,
        "items": saved_items,
        "created_at_local": str(entry_date)
    }

def update_food_entry(user_id: int, entry_date: date, entry_code: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Updates an existing food entry identified by entry_code.
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    query_find = "SELECT id FROM food_entry WHERE day_session_id = %s AND entry_code = %s AND is_deleted = FALSE"
    row = fetch_one(query_find, (session_id, entry_code))
    if not row:
        return None
    
    entry_db_id = row['id']
    
    if 'meal' in updates or 'intake_kcal' in updates:
        # Build dynamic update query
        fields = []
        params = []
        if 'meal' in updates:
            fields.append("meal = %s")
            params.append(updates['meal'])
        if 'intake_kcal' in updates:
            fields.append("intake_kcal = %s")
            params.append(updates['intake_kcal'])
            
        params.append(entry_db_id)
        query_update = f"UPDATE food_entry SET {', '.join(fields)} WHERE id = %s"
        execute(query_update, tuple(params))
        
    if 'items' in updates:
        # Get existing items
        existing_items_query = "SELECT id FROM food_item WHERE food_entry_id = %s ORDER BY id"
        existing_items = fetch_all(existing_items_query, (entry_db_id,))
        existing_ids = [item['id'] for item in existing_items]
        
        new_items = updates['items']
        
        # Update existing items or insert new ones
        for idx, item in enumerate(new_items):
            qty = item.get('qty')
            if qty == 'UNKNOWN': 
                qty = None
            
            kcal = item.get('kcal', 0)
            
            if idx < len(existing_ids):
                # UPDATE existing item
                item_id = existing_ids[idx]
                query_update = """
                    UPDATE food_item 
                    SET item_name = %s, qty = %s, unit = %s, kcal = %s, note = %s
                    WHERE id = %s
                """
                execute(query_update, (
                    item.get('name'), 
                    qty, 
                    item.get('unit'), 
                    kcal, 
                    item.get('note'),
                    item_id
                ))
            else:
                # INSERT new item (if there are more new items than existing)
                query_item = """
                    INSERT INTO food_item (food_entry_id, item_name, qty, unit, kcal, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                execute(query_item, (
                    entry_db_id, 
                    item.get('name'), 
                    qty, 
                    item.get('unit'), 
                    kcal, 
                    item.get('note')
                ))
        
        # DELETE extra items if new list is shorter than existing
        if len(new_items) < len(existing_ids):
            ids_to_delete = existing_ids[len(new_items):]
            placeholders = ','.join(['%s'] * len(ids_to_delete))
            delete_query = f"DELETE FROM food_item WHERE id IN ({placeholders})"
            execute(delete_query, tuple(ids_to_delete))

    return _get_food_entry_details(entry_db_id)

def add_items_to_food_entry(user_id: int, entry_date: date, entry_code: str, new_items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Appends items to an existing food entry.
    """
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    query_find = "SELECT id FROM food_entry WHERE day_session_id = %s AND entry_code = %s AND is_deleted = FALSE"
    row = fetch_one(query_find, (session_id, entry_code))
    if not row:
        return None
        
    entry_db_id = row['id']
    
    for item in new_items:
            query_item = """
            INSERT INTO food_item (food_entry_id, item_name, qty, unit, note)
            VALUES (%s, %s, %s, %s, %s)
        """
            qty = item.get('qty')
            if qty == 'UNKNOWN': qty = None
            execute(query_item, (entry_db_id, item.get('name'), qty, item.get('unit'), item.get('note')))
            
    return _get_food_entry_details(entry_db_id)

def delete_food_entry(user_id: int, entry_date: date, entry_code: str) -> bool:
    session_id = get_or_create_day_session(user_id, str(entry_date))
    
    query_find = "SELECT id FROM food_entry WHERE day_session_id = %s AND entry_code = %s"
    row = fetch_one(query_find, (session_id, entry_code))
    if not row:
        return False
        
    entry_db_id = row['id']
    execute("UPDATE food_entry SET is_deleted = TRUE WHERE id = %s", (entry_db_id,))
    return True

def _get_food_entry_details(entry_db_id: int) -> Dict[str, Any]:
    query_entry = "SELECT * FROM food_entry WHERE id = %s"
    entry_row = fetch_one(query_entry, (entry_db_id,))
    if not entry_row:
        return {}
        
    query_items = "SELECT * FROM food_item WHERE food_entry_id = %s"
    items_rows = fetch_all(query_items, (entry_db_id,))
    
    items = []
    for ir in items_rows:
        items.append({
            "id": ir['id'],
            "name": ir['item_name'],
            "qty": float(ir['qty']) if ir['qty'] else None,
            "unit": ir['unit'],
            "kcal": float(ir['kcal']) if ir['kcal'] else 0.0,
            "note": ir['note']
        })
        
    return {
        "id": entry_row['id'],
        "entry_code": entry_row['entry_code'],
        "meal": entry_row['meal'],
        "action": entry_row['action'],
        "intake_kcal": float(entry_row['intake_kcal']) if entry_row['intake_kcal'] else 0.0,
        "items": items,
        "created_at_local": str(entry_row['created_at'])
    }

def delete_food_entry_by_id(entry_id: int) -> bool:
    execute("UPDATE food_entry SET is_deleted = TRUE WHERE id = %s", (entry_id,))
    return True

# --- Fetch Functions (Added for StatsService) ---

def get_day_food_entries(user_id: int, entry_date: date) -> List[Dict[str, Any]]:
    """
    Get all food entries for a specific day.
    """
    session_id = get_day_session_id(user_id, str(entry_date))
    if not session_id:
        return []
    
    query = """
        SELECT fe.id, fe.entry_code, fe.meal, fe.intake_kcal, fe.created_at
        FROM food_entry fe 
        WHERE fe.day_session_id = %s AND fe.is_deleted = FALSE 
        ORDER BY fe.created_at ASC
    """
    rows = fetch_all(query, (session_id,))
    
    results = []
    for r in rows:
        details = _get_food_entry_details(r['id'])
        for item in details['items']:
            results.append({
                "id": item['id'], # Use Item ID for uniqueness in lists
                "entry_id": details['id'], # Keep parent ID reference
                "name": item['name'],
                "kcal": item['kcal'],
                "quantity": item['qty'],
                "unit": item['unit'],
                "time": details['created_at_local']
            })
            
    return results

def get_food_entries_in_range(user_id: int, start_date: date, end_date: date) -> List[Dict[str, Any]]:
    """
    Get all food entries within a date range (inclusive), grouped by date.
    Returns list of objects: { "date": date_obj, "entries": [...] }
    """
    # Join day_session to filter by date range
    query = """
        SELECT ds.entry_date, fe.id, fe.intake_kcal
        FROM day_session ds
        JOIN food_entry fe ON fe.day_session_id = ds.id
        WHERE ds.user_id = %s AND ds.entry_date >= %s AND ds.entry_date <= %s AND fe.is_deleted = FALSE
    """
    rows = fetch_all(query, (user_id, start_date, end_date))
    
    by_date = {}
    for r in rows:
        d_str = str(r['entry_date'])
        if d_str not in by_date:
            by_date[d_str] = []
        
        by_date[d_str].append({
            "kcal": float(r['intake_kcal'])
        })
        
    return by_date
