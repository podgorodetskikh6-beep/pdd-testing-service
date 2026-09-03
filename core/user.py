from repository.user import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    def create_user(self, username: str) -> int:
        username = username.strip()

        if not username:
            return False

        return self.repo.create_user(username)