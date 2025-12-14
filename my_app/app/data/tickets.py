import pandas as pd

def insert_ticket(conn, title, description, priority, status):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets (title, description, priority, status)
        VALUES (?, ?, ?, ?)
    """, (title, description, priority, status))

    conn.commit()
    return cursor.lastrowid


def get_all_tickets(conn):
    return pd.read_sql_query("SELECT * FROM it_tickets", conn)
