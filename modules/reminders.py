from database import get_connection


def add_reminder(title, reminder_time):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO reminders (title, reminder_time)
        VALUES (?, ?)
    """, (title.strip(), reminder_time))

    reminder_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return reminder_id


def get_reminders():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM reminders
        ORDER BY reminder_time ASC
    """).fetchall()

    connection.close()

    return rows


def complete_reminder(reminder_id):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE reminders
        SET completed = 1
        WHERE id = ?
    """, (reminder_id,))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


def delete_reminder(reminder_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success