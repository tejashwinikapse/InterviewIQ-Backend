import sqlite3


def create_table():
    connection = sqlite3.connect("interview_history.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS interview_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_interview(role, question, answer, feedback):
    connection = sqlite3.connect("interview_history.db")

    connection.execute("""
        INSERT INTO interview_history
        (role, question, answer, feedback)
        VALUES (?, ?, ?, ?)
    """, (role, question, answer, feedback))

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect("interview_history.db")
    connection.row_factory = sqlite3.Row

    rows = connection.execute("""
        SELECT * FROM interview_history ORDER BY id DESC
    """).fetchall()

    history = [dict(row) for row in rows]
    connection.close()

    return history