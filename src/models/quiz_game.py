import json
from pathlib import Path

from src.data import build_default_quizzes
from src.models.quiz import Quiz


class QuizGame:
    """Game container with default quizzes loaded on startup."""

    def __init__(self, state_file_path: str | Path = "state.json") -> None:
        self.quizzes: list[Quiz] = build_default_quizzes()
        self.best_score = 0
        self.history: list[dict] = []
        self._is_running = True
        self.state_file_path = Path(state_file_path)
        self.load_state()

    def show_menu(self) -> None:
        print("\n=== Quiz Game ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def get_menu_choice(self) -> int | None:
        while True:
            try:
                raw = input("메뉴를 선택하세요 (1-5): ").strip()
            except (KeyboardInterrupt, EOFError):
                self._handle_safe_shutdown()
                return None

            if not raw:
                print("입력을 확인해주세요. 비어 있는 값은 사용할 수 없습니다.")
                continue

            try:
                choice = int(raw)
            except ValueError:
                print("숫자로 입력해주세요.")
                continue

            if choice < 1 or choice > 5:
                print("1에서 5 사이 숫자를 입력해주세요.")
                continue
            return choice

    def save_state(self) -> None:
        payload = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with self.state_file_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
        except OSError:
            print("상태 저장에 실패했습니다. 다음 실행 시 복구를 시도합니다.")

    def load_state(self) -> None:
        if not self.state_file_path.exists():
            return

        try:
            with self.state_file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data["quizzes"]
            best_score = data["best_score"]
            if not isinstance(quizzes_data, list) or not isinstance(best_score, int):
                raise ValueError("invalid state schema")

            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            self.best_score = best_score
        except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError):
            print("상태 파일을 읽을 수 없어 기본 데이터로 복구합니다.")
            self.quizzes = build_default_quizzes()
            self.best_score = 0

    def _handle_safe_shutdown(self) -> None:
        print("\n입력이 중단되어 프로그램을 안전하게 종료합니다.")
        try:
            self.save_state()
        except Exception:
            print("저장 중 문제가 발생했지만 프로그램은 안전하게 종료됩니다.")
        self._is_running = False

    def play_quiz(self) -> None:
        print("퀴즈 풀기 기능은 다음 단계에서 구현됩니다.")

    def add_quiz(self) -> None:
        print("퀴즈 추가 기능은 다음 단계에서 구현됩니다.")

    def list_quizzes(self) -> None:
        print("퀴즈 목록 기능은 다음 단계에서 구현됩니다.")

    def show_best_score(self) -> None:
        print(f"현재 최고 점수: {self.best_score}")

    def _dispatch_menu(self, choice: int) -> None:
        if choice == 1:
            self.play_quiz()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.list_quizzes()
        elif choice == 4:
            self.show_best_score()
        elif choice == 5:
            print("프로그램을 종료합니다.")
            self._is_running = False

    def run(self) -> None:
        print("프로그램을 시작합니다.")
        try:
            while self._is_running:
                self.show_menu()
                choice = self.get_menu_choice()
                if choice is None:
                    break
                self._dispatch_menu(choice)
        except (KeyboardInterrupt, EOFError):
            self._handle_safe_shutdown()
