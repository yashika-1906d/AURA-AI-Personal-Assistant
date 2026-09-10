from database import get_connection


def add_task(title, priority="Medium"):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO tasks (title, priority)
        VALUES (?, ?)
    """, (title.strip(), priority))

    task_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return task_id


def get_tasks(show_completed=True):
    connection = get_connection()

    if show_completed:
        rows = connection.execute("""
            SELECT *
            FROM tasks
            ORDER BY completed ASC, created_at DESC
        """).fetchall()
    else:
        rows = connection.execute("""
            SELECT *
            FROM tasks
            WHERE completed = 0
            ORDER BY created_at DESC
        """).fetchall()

    connection.close()

    return rows


def complete_task(task_id):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE tasks
        SET completed = 1,
            completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (task_id,))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


def delete_task(task_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


def update_task_priority(task_id, priority):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE tasks
        SET priority = ?
        WHERE id = ?
    """, (priority, task_id))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


def get_task_statistics():
    connection = get_connection()

    total = connection.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    pending = total - completed

    connection.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }