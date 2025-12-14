from app.data.db import connect_database

def initialize_database():
    conn = connect_database()
    cursor = conn.cursor()

    # USERS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT
    )
    """)

    # INCIDENTS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reporter TEXT
    )
    """)

    # DATASETS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        owner TEXT,
        records INTEGER
    )
    """)

    # TICKETS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        issue TEXT,
        priority TEXT,
        status TEXT,
        reporter TEXT
    )
    """)

    conn.commit()
    conn.close()
