import json
import sqlite3
from repository.migration import migrate

DB_PATH = "pdd.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def seed_ticket2():
    with open("ticket2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    ticket_number = data["ticket"]
    questions = data["questions"]

    with get_connection() as conn:
        cursor = conn.cursor()

        # =========================
        # 1. ticket
        # =========================
        cursor.execute(
            "INSERT INTO tickets (title) VALUES (?)",
            (f"Ticket {ticket_number}",)
        )
        ticket_id = cursor.lastrowid

        # =========================
        # 2. questions + variants
        # =========================
        for q in questions:

            # insert question
            cursor.execute("""
                INSERT INTO questions (
                    ticket_id,
                    text,
                    correct_answer,
                    image_path
                )
                VALUES (?, ?, ?, ?)
            """, (
                ticket_id,
                q["text"],
                q["answer"],
                q["image"]
            ))

            question_id = cursor.lastrowid

            # insert variants (ВАЖНО — отдельная таблица)
            for v in q["variants"]:
                cursor.execute("""
                    INSERT INTO question_variants (
                        question_id,
                        variant_text
                    )
                    VALUES (?, ?)
                """, (
                    question_id,
                    v
                ))

        conn.commit()

    print(f"Ticket {ticket_number} inserted successfully (id={ticket_id})")


if __name__ == "__main__":
    migrate()
    seed_ticket2()