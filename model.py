from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Question:
    id: int | None
    ticket_id: int
    text: str
    variants: List[str]
    correct_answer: str
    image_path: Optional[str]


@dataclass
class Ticket:
    id: int | None
    title: str
    questions: List[Question]


@dataclass
class User:
    id: int | None
    username: str


@dataclass
class Stat:
    id: int | None
    user_id: int
    ticket_id: int
    correct_answers: int
    total_questions: int
