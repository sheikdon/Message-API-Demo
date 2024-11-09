from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Reminder for running FastAPI
# To start, type in terminal: uvicorn main:app --reload
# Access live server documentation: http://127.0.0.1:8000/docs

app = FastAPI()

# Define message model
class Message(BaseModel):
    sender: str
    message: str

# Helper function to interact with the database
def send_message_to_db(sender_username, message_text):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # Insert user if they don't exist
    c.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (sender_username,))
    conn.commit()

    # Get sender ID
    c.execute('SELECT id FROM users WHERE username = ?', (sender_username,))
    sender_id = c.fetchone()[0]

    # Insert message
    c.execute('INSERT INTO messages (sender_id, message) VALUES (?, ?)', (sender_id, message_text))
    conn.commit()
    conn.close()

# Fetch messages from the database
def get_messages_from_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
    SELECT users.username, messages.message, messages.timestamp 
    FROM messages JOIN users ON messages.sender_id = users.id
    ORDER BY messages.timestamp DESC 
    ''')
    messages = c.fetchall()
    conn.close()
    return [{"sender": sender, "message": msg, "timestamp": ts} for sender, msg, ts in messages]

# API Endpoints
@app.post("/send_message/")
async def send_message(msg: Message):
    try:
        send_message_to_db(msg.sender, msg.message)
        return {"status": "Message sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_messages/")
async def get_messages():
    try:
        messages = get_messages_from_db()
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#if i want to send a message thru terminal:
    '''
    curl -X 'POST' \
  'http://127.0.0.1:8000/send_message/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "sender": "alice",
    "message": "Hello from curl!"
  }'
  '''

#check thru terminal
 # sqlite3 messages.db

# View all messages along with the corresponding usernames
'''
SELECT users.username, messages.message, messages.timestamp 
FROM messages 
JOIN users ON messages.sender_id = users.id 
ORDER BY messages.timestamp DESC;
'''
# Exit SQLite when done
# .exit

#OTHER COMMANDS:
# --- SQLite Commands ---
'''
# Open the Database
sqlite3 messages.db

# List All Tables in the Database
.tables

# Describe the Structure of a Table
.schema table_name
# Example: .schema users

# Show All Data in a Table
SELECT * FROM table_name;
# Example: SELECT * FROM users;

# Query with Filters
SELECT * FROM messages WHERE sender_id = 1;

# Limit the Results
SELECT * FROM messages LIMIT 10;

# Order the Results by Timestamp (Descending)
SELECT * FROM messages ORDER BY timestamp DESC;

# Count the Rows in a Table
SELECT COUNT(*) FROM messages;

# Exit SQLite
.exit


# --- Advanced SQLite Commands ---

# Create a Table
CREATE TABLE table_name (
    column1_name column1_type,
    column2_name column2_type
);
# Example: CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE);

# Insert Data into a Table
INSERT INTO table_name (column1, column2) VALUES (value1, value2);
# Example: INSERT INTO users (username) VALUES ('alice');

# Update Data in a Table
UPDATE table_name SET column_name = new_value WHERE condition;
# Example: UPDATE users SET username = 'bob' WHERE id = 1;

# Delete Data from a Table
DELETE FROM table_name WHERE condition;
# Example: DELETE FROM users WHERE username = 'alice';

# Backup the Database
.backup 'backup_messages.db'

# Import Data from CSV
.mode csv
.import your_file.csv table_name

# Export Data to CSV
.mode csv
.output your_file.csv
SELECT * FROM table_name;
.output stdout
'''