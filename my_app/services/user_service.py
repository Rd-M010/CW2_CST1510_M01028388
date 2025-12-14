def migrate_users_from_file(conn):
    cursor = conn.cursor()

    with open("DATA/users.txt") as f:
        users = f.readlines()

    count = 0
    for line in users:
        username = line.strip()
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, "placeholder", "user")
        )
        count += 1

    conn.commit()
    return count
