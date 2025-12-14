import pandas as pd

def insert_dataset(conn, dataset_name, domain, num_rows, num_columns):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (dataset_name, domain, num_rows, num_columns)
        VALUES (?, ?, ?, ?)
    """, (dataset_name, domain, num_rows, num_columns))

    conn.commit()
    return cursor.lastrowid


def get_all_datasets(conn):
    return pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
