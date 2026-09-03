from typing import Optional
from repository.repository import SQLiteRepository

from model import Ticket, Question


class TestRepository(SQLiteRepository):

    def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, title FROM tickets WHERE id=?",
                (ticket_id,)
            )
            t_row = cursor.fetchone()

            if not t_row:
                return None

            cursor.execute(
                "SELECT id, ticket_id, text, correct_answer, image_path "
                "FROM questions WHERE ticket_id=?",
                (ticket_id,)
            )

            questions = []

            for q_row in cursor.fetchall():
                cursor.execute(
                    """
                    SELECT variant_text
                    FROM question_variants
                    WHERE question_id=?
                    """,
                    (q_row["id"],)
                )

                variants = [v["variant_text"] for v in cursor.fetchall()]

                questions.append(
                    Question(
                        id=q_row["id"],
                        ticket_id=q_row["ticket_id"],
                        text=q_row["text"],
                        variants=variants,
                        correct_answer=q_row["correct_answer"],
                        image_path=q_row["image_path"]
                    )
                )

            return Ticket(
                id=t_row["id"],
                title=t_row["title"],
                questions=questions
            )

    def get_ticket_ids(self) -> list[int]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM tickets")
            return [row["id"] for row in cursor.fetchall()]