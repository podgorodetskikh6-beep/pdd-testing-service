from repository.repository import SQLiteRepository

class StatsRepository(SQLiteRepository):

    def save_result(self, user_id: int, ticket_id: int, correct: int, total: int):
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO stats (
                    user_id,
                    ticket_id,
                    correct_answers,
                    total_questions
                )
                VALUES (?, ?, ?, ?)
            """, (user_id, ticket_id, correct, total))

            conn.commit()

    def get_user_stats(self, user_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM stats
                WHERE user_id=?
                ORDER BY completed_at DESC
            """, (user_id,))

            return cursor.fetchall()