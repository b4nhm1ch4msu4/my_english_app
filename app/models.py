from dataclasses import dataclass
from datetime import date, timedelta
from app.sm_2_algo import SM2Algorithm, Quality


@dataclass
class Word:
    word: str
    part_of_speech: str
    phonetic: str
    audio: str
    meaning: str
    example: str


@dataclass
class ReviewStatus(SM2Algorithm):
    repetitions: int
    ease_factor: float
    interval: int
    next_review: date

    def __init__(
        self, repetitions: int, ease_factor: float, interval: int, next_review: date
    ) -> None:
        super().__init__(repetitions, ease_factor, interval)
        self.next_review = next_review

    def update(self, q: Quality):
        super().update(q)
        self.next_review += timedelta(days=self.interval)


def default_review_status() -> ReviewStatus:
    return ReviewStatus(0, 2.5, 0, next_review=date.today() + timedelta(days=1))
