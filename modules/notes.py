from database import get_connection


def add_note(title, content):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO notes (title, content)
        VALUES (?, ?)
    """, (title.strip(), content.strip()))

    note_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return note_id


def get_notes():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM notes
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return rows


def get_note(note_id):
    connection = get_connection()

    row = connection.execute("""
        SELECT *
        FROM notes
        WHERE id = ?
    """, (note_id,)).fetchone()

    connection.close()

    return row


def update_note(note_id, title, content):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE notes
        SET title = ?,
            content = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title.strip(), content.strip(), note_id))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


def delete_note(note_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM notes
        WHERE id = ?
    """, (note_id,))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


def search_notes(keyword):
    connection = get_connection()

    search_value = f"%{keyword}%"

    rows = connection.execute("""
        SELECT *
        FROM notes
        WHERE title LIKE ?
        OR content LIKE ?
        ORDER BY created_at DESC
    """, (search_value, search_value)).fetchall()

    connection.close()

    return rows