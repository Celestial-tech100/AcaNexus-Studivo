import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/acanexus.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS profiles;

CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    university TEXT,
    course TEXT,
    branch TEXT,
    year TEXT,
    semester TEXT,
    session TEXT,
    bio TEXT
);
""")

conn.commit()
conn.close()

print("Database reset complete")