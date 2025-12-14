import sqlite3

def init_db():
    conn = sqlite3.connect("database/platform.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized: users table ready")

if __name__ == "__main__":
    init_db()

