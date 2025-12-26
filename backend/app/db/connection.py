import os
import MySQLdb
from MySQLdb.cursors import DictCursor
from dotenv import load_dotenv
from typing import Optional, Any, List, Dict, Generator
from contextlib import contextmanager
from pathlib import Path

# Load environment variables from .env file
# Try to find .env in backend directory (handles running from project root)
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Fallback to default search
    load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "calorie_db")
DB_PORT = int(os.getenv("DB_PORT", 3307))

if not DB_USER or not DB_PASSWORD:
    raise ValueError("DB_USER and DB_PASSWORD must be set in the .env file.")

def get_connection():
    """Create a new database connection."""
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        port=DB_PORT,
        cursorclass=DictCursor,
        charset='utf8mb4',
        init_command="SET time_zone='+07:00'"
    )

@contextmanager
def get_db_cursor(commit: bool = False) -> Generator:
    """Context manager for database cursor. Handles connection open/close and commit/rollback."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_one(query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
    """Fetch a single row from the database."""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

def fetch_all(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """Fetch all rows from the database."""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def execute(query: str, params: Optional[tuple] = None) -> int:
    """Execute a query (INSERT, UPDATE, DELETE). Returns lastrowid for INSERT, or rowcount."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, params)
        if query.strip().upper().startswith("INSERT"):
            return cursor.lastrowid
        return cursor.rowcount

def execute_many(query: str, params_list: List[tuple]) -> int:
    """Execute a batch query. Returns total rowcount."""
    with get_db_cursor(commit=True) as cursor:
        cursor.executemany(query, params_list)
        return cursor.rowcount
