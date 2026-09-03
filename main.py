from repository.stats import StatsRepository
from core.stats import StatsService
from ui import UI

from repository.test import TestRepository
from repository.user import UserRepository
from core.user import UserService


def main():
    test_repo = TestRepository()
    user_repo = UserRepository()
    stats_repo = StatsRepository()

    stats_service = StatsService(stats_repo)
    user_service = UserService(user_repo)

    ticket = test_repo.get_ticket(1)

    if not ticket:
        print("Ticket not found")
        return

    ui = UI(
        exam_factory=test_repo,
        user_service=user_service,
        stats_service=stats_service
    )

    ui.run()


if __name__ == "__main__":
    main()