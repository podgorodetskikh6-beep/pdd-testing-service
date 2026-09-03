import sqlite3


DB_PATH = "pdd.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def migrate():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            image_path TEXT,

            FOREIGN KEY (ticket_id)
                REFERENCES tickets(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS question_variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            variant_text TEXT NOT NULL,

            FOREIGN KEY (question_id)
                REFERENCES questions(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ticket_id INTEGER NOT NULL,
            correct_answers INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (ticket_id)
                REFERENCES tickets(id)
                ON DELETE CASCADE
        );
        """)

        conn.commit()

if __name__ == "__main__":
    migrate()
    print(" Migration completed")