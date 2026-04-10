import sqlite3
import datetime

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    user TEXT,
    item TEXT,
    location TEXT,
    timestamp TEXT,
    confidence REAL,
    image TEXT
)
""")
conn.commit()

def add_item(user, item, location, image_path=None):
    cursor.execute(
        "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)",
        (user, item, location, str(datetime.datetime.now()), 0.9, image_path)
    )
    conn.commit()

def get_items(user, item):
    cursor.execute(
        "SELECT * FROM items WHERE user=? AND item=?",
        (user, item)
    )
    return cursor.fetchall()