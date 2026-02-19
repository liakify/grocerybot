"""Database operations for GroceryBot."""
import sqlite3
from contextlib import contextmanager
from typing import List, Optional, Tuple

import config


@contextmanager
def get_connection():
    """Get database connection with context manager."""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database() -> None:
    """Initialize the database with required tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grocery_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                item TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, item)
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chat_id ON grocery_items(chat_id)
        """)
        # Add completed column if it doesn't exist (for existing databases)
        cursor.execute("PRAGMA table_info(grocery_items)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'completed' not in columns:
            cursor.execute("ALTER TABLE grocery_items ADD COLUMN completed INTEGER DEFAULT 0")


def add_item(chat_id: int, item: str) -> bool:
    """Add an item to the grocery list for a specific chat.
    
    Returns:
        True if item was added, False if it already exists.
    """
    original_item = item.strip()
    item_lower = original_item.lower()
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Check if item already exists (case-insensitive)
            cursor.execute(
                "SELECT id FROM grocery_items WHERE chat_id = ? AND LOWER(item) = ?",
                (chat_id, item_lower)
            )
            if cursor.fetchone():
                return False
            
            # Insert the item with original case
            cursor.execute(
                "INSERT INTO grocery_items (chat_id, item) VALUES (?, ?)",
                (chat_id, original_item)
            )
        return True
    except sqlite3.IntegrityError:
        return False


def add_items(chat_id: int, items: List[str]) -> Tuple[int, int]:
    """Add multiple items to the grocery list.
    
    Returns:
        Tuple of (added_count, existing_count)
    """
    added = 0
    existing = 0
    
    for item in items:
        if add_item(chat_id, item):
            added += 1
        else:
            existing += 1
    
    return added, existing


def get_items(chat_id: int) -> List[sqlite3.Row]:
    """Get all items in the grocery list for a specific chat."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, item, added_at, completed FROM grocery_items WHERE chat_id = ? ORDER BY id",
            (chat_id,)
        )
        return cursor.fetchall()


def clear_list(chat_id: int) -> int:
    """Clear all items from the grocery list.
    
    Returns:
        Number of items removed.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grocery_items WHERE chat_id = ?", (chat_id,))
        return cursor.rowcount


def get_item_count(chat_id: int) -> int:
    """Get the count of items in the grocery list."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM grocery_items WHERE chat_id = ?",
            (chat_id,)
        )
        return cursor.fetchone()[0]


def toggle_item_completed(chat_id: int, item_id: int) -> Optional[str]:
    """Toggle the completed status of an item.
    
    Returns:
        The new completed status (True/False), or None if item not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        # First get current status
        cursor.execute(
            "SELECT item, completed FROM grocery_items WHERE chat_id = ? AND id = ?",
            (chat_id, item_id)
        )
        row = cursor.fetchone()
        if not row:
            return None
        
        new_status = 1 if row[1] == 0 else 0
        cursor.execute(
            "UPDATE grocery_items SET completed = ? WHERE chat_id = ? AND id = ?",
            (new_status, chat_id, item_id)
        )
        return new_status == 1


def remove_item_by_id(chat_id: int, item_id: int) -> Optional[str]:
    """Remove an item by its ID.
    
    Returns:
        The removed item name, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT item FROM grocery_items WHERE chat_id = ? AND id = ?",
            (chat_id, item_id)
        )
        row = cursor.fetchone()
        if not row:
            return None
        
        item_name = row[0]
        cursor.execute(
            "DELETE FROM grocery_items WHERE chat_id = ? AND id = ?",
            (chat_id, item_id)
        )
        return item_name
