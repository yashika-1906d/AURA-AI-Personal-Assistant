import sqlite3
from pathlib import Path

from config import DATABASE_PATH


def get_connection():
    database = Path(DATABASE_PATH)

    # Create the data folder if it doesn't exist
    database.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database)

    # Allows us to access database columns by name
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------------
    # TASKS TABLE
    # -------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'Medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)

    # -------------------------------
    # NOTES TABLE
    # -------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------------
    # REMINDERS TABLE
    # -------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------------
    # CONVERSATIONS TABLE
    # -------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            assistant_response TEXT NOT NULL,
            intent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_conversation(user_message, assistant_response, intent):

    connection = get_connection()

    connection.execute("""
        INSERT INTO conversations
        (user_message, assistant_response, intent)
        VALUES (?, ?, ?)
    """, (
        user_message,
        assistant_response,
        intent
    ))

    connection.commit()
    connection.close()


def get_conversations(limit=50):

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    connection.close()

    return rows


if __name__ == "__main__":

    initialize_database()

    print("AURA database initialized successfully!")