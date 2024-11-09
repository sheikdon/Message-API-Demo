import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('messages.db')
c = conn.cursor()

# Create the users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE
)
''')

# Create the messages table with a foreign key reference to users
c.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
