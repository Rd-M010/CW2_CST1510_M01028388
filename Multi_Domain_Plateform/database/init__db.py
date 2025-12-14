import sqlite3

conn = sqlite3.connect("database/platform.db")
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# SECURITY INCIDENTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS security_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_type TEXT,
    severity TEXT,
    status TEXT,
    description TEXT
)
""")

# SAMPLE INCIDENTS
cur.execute("""
INSERT INTO security_incidents (incident_type, severity, status, description)
VALUES
('Phishing', 'High', 'Open', 'Suspicious email reported'),
('Malware', 'Critical', 'Investigating', 'Ransomware detected'),
('DDoS', 'Medium', 'Resolved', 'Temporary service outage')
""")

conn.commit()
conn.close()

print("Database initialized")
