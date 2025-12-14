import sqlite3
from pathlib import Path

# Path to this file: my_app/app/data/db.py
CURRENT_DIR = Path(__file__).resolve().parent

# The database file will be stored NEXT TO db.py
DB_PATH = CURRENT_DIR / "intelligence_platform.db"

def connect_database():
    """
    Connect to the SQLite database.
    Creates the database file if it does not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    return conn
