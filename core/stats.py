from repository.stats import StatsRepository


class StatsService:
    def __init__(self, repo: StatsRepository):
        self.repo = repo

    def save_result(self, user_id, ticket_id, correct, total):
        self.repo.save_result(user_id, ticket_id, correct, total)

    def get_stats(self, user_id):
        return self.repo.get_user_stats(user_id)