from src.data import build_default_quizzes
from src.models.quiz import Quiz


class QuizGame:
    """Game container with default quizzes loaded on startup."""

    def __init__(self) -> None:
        self.quizzes: list[Quiz] = build_default_quizzes()
        self.best_score = 0
        self.history: list[dict] = []

    def run(self) -> None:
        print("=== Quiz Game ===")
        print("프로그램을 시작합니다.")
        print(f"기본 퀴즈 {len(self.quizzes)}개가 준비되었습니다.")
        print("프로그램을 종료합니다.")
