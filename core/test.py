from model import Ticket


class TestService:
    def __init__(self, ticket: Ticket, max_errors: int = 2):
        self.ticket = ticket
        self.questions = ticket.questions
        self.current_index = 0
        self.correct = 0
        self.errors = 0
        self.error_details = []
        self.max_errors = max_errors

    def get_current_question(self):
        if self.is_finished():
            return None
        return self.questions[self.current_index]

    def answer(self, user_answer: str) -> bool:
        q = self.get_current_question()
        if not q:
            return False
        is_correct = (q.correct_answer == user_answer)

        if is_correct:
            self.correct += 1
        else:
            self.errors += 1
            self.error_details.append({
                "text": q.text,
                "your": user_answer,
                "correct": q.correct_answer
            })

        self.current_index += 1

        return is_correct

    def is_finished(self) -> bool:
        return (
            self.current_index >= len(self.questions)
            or self.errors >= self.max_errors
        )

    def result(self) -> dict:
        return {
            "ticket": self.ticket.id,
            "correct": self.correct,
            "errors": self.errors,
            "total": len(self.questions),
            "passed": self.errors < self.max_errors,
            "error_details": self.error_details
        }
    def finish_reason(self) -> str:
        if self.errors >= self.max_errors:
            return "Превышено количество ошибок"
        return "Тест завершён успешно"

    def get_progress(self):
        return self.current_index + 1, len(self.questions)