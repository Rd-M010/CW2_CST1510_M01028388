from app.data.db import connect_database

conn = connect_database()
print("Database connected:", conn)
conn.close()

