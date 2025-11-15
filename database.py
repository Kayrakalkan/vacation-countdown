import sqlite3
import os
from datetime import datetime

# Use persistent storage on Render if DATA_DIR is set, otherwise use current directory
DATA_DIR = os.environ.get('DATA_DIR', '.')
DATABASE_NAME = os.path.join(DATA_DIR, 'vacations.db')

# Debug: Print database location on startup
print(f"[DATABASE] Using DATA_DIR: {DATA_DIR}")
print(f"[DATABASE] Database location: {DATABASE_NAME}")
print(f"[DATABASE] Database exists: {os.path.exists(DATABASE_NAME)}")
if os.path.exists(DATA_DIR):
    print(f"[DATABASE] DATA_DIR is writable: {os.access(DATA_DIR, os.W_OK)}")
else:
    print(f"[DATABASE] WARNING: DATA_DIR does not exist!")

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the vacations table."""
    print(f"[INIT_DB] Creating/checking database at: {DATABASE_NAME}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create vacations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            start_date DATE NOT NULL,
            notes TEXT,
            is_active BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Check how many vacations exist
    count = cursor.execute('SELECT COUNT(*) FROM vacations').fetchone()[0]
    print(f"[INIT_DB] Database initialized! Current vacation count: {count}")
    
    conn.close()
    print("Database initialized successfully!")

def add_vacation(location, start_date, notes='', is_active=False):
    """Add a new vacation to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # If this vacation is being set as active, deactivate all others
    if is_active:
        cursor.execute('UPDATE vacations SET is_active = 0')
    
    cursor.execute('''
        INSERT INTO vacations (location, start_date, notes, is_active)
        VALUES (?, ?, ?, ?)
    ''', (location, start_date, notes, 1 if is_active else 0))
    
    conn.commit()
    vacation_id = cursor.lastrowid
    conn.close()
    return vacation_id

def get_all_vacations():
    """Retrieve all vacations."""
    conn = get_db_connection()
    vacations = conn.execute('''
        SELECT * FROM vacations 
        ORDER BY start_date ASC
    ''').fetchall()
    conn.close()
    return vacations

def get_active_vacation():
    """Get the active vacation."""
    conn = get_db_connection()
    vacation = conn.execute('''
        SELECT * FROM vacations 
        WHERE is_active = 1
        LIMIT 1
    ''').fetchone()
    conn.close()
    return vacation

def get_vacation_by_id(vacation_id):
    """Get a specific vacation by ID."""
    conn = get_db_connection()
    vacation = conn.execute('''
        SELECT * FROM vacations 
        WHERE id = ?
    ''', (vacation_id,)).fetchone()
    conn.close()
    return vacation

def update_vacation_notes(vacation_id, notes):
    """Update notes for a specific vacation."""
    conn = get_db_connection()
    conn.execute('''
        UPDATE vacations 
        SET notes = ? 
        WHERE id = ?
    ''', (notes, vacation_id))
    conn.commit()
    conn.close()

def set_active_vacation(vacation_id):
    """Set a vacation as active and deactivate all others."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Deactivate all vacations
    cursor.execute('UPDATE vacations SET is_active = 0')
    
    # Activate the selected vacation
    cursor.execute('''
        UPDATE vacations 
        SET is_active = 1 
        WHERE id = ?
    ''', (vacation_id,))
    
    conn.commit()
    conn.close()

def delete_vacation(vacation_id):
    """Delete a vacation by ID."""
    conn = get_db_connection()
    conn.execute('DELETE FROM vacations WHERE id = ?', (vacation_id,))
    conn.commit()
    conn.close()

def calculate_days_remaining(start_date_str):
    """Calculate days remaining until vacation."""
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        delta = start_date - today
        return delta.days
    except Exception as e:
        print(f"Error calculating days: {e}")
        return None

if __name__ == '__main__':
    # Initialize the database when this script is run directly
    init_db()
