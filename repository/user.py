from repository.repository import SQLiteRepository
class UserRepository(SQLiteRepository):
    def create_user(self, username: str) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT OR IGNORE INTO users (username) VALUES (?)",
                (username,)
            )

            cursor.execute(
                "SELECT id FROM users WHERE username=?",
                (username,)
            )

            return cursor.fetchone()["id"]