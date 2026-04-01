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
            if not 1 <= choice <= 5:
                print("1에서 5 사이 숫자를 입력해주세요.")
                continue
            return choice

    def _get_quiz_answer(self) -> int | None:
        while True:
            try:
                raw = input("정답 번호를 입력하세요 (1-4): ").strip()
            except (KeyboardInterrupt, EOFError):
                self._handle_safe_shutdown()
                return None

            if not raw:
                print("입력을 확인해주세요. 비어 있는 값은 사용할 수 없습니다.")
                continue
            try:
                answer = int(raw)
            except ValueError:
                print("숫자로 입력해주세요.")
                continue
            if not 1 <= answer <= 4:
                print("1에서 4 사이 숫자를 입력해주세요.")
                continue
            return answer

    def load_state(self) -> None:
        if not self.state_file_path.exists():
            return
        try:
            data = json.loads(self.state_file_path.read_text(encoding="utf-8"))
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

    def save_state(self) -> None:
        payload = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            self.state_file_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError:
            print("상태 저장에 실패했습니다.")

    def _handle_safe_shutdown(self) -> None:
        print("\n입력이 중단되어 프로그램을 안전하게 종료합니다.")
        try:
            self.save_state()
        except Exception:
            print("저장 중 문제가 발생했지만 프로그램은 안전하게 종료됩니다.")
        self._is_running = False

    def play_quiz(self) -> None:
        if not self.quizzes:
            print("출제할 퀴즈가 없습니다.")
            return

        correct_count = 0
        total = len(self.quizzes)

        for index, quiz in enumerate(self.quizzes, start=1):
            if not self._is_running:
                return

            print(f"\n[{index}/{total}]")
            print(quiz.format_question())
            user_answer = self._get_quiz_answer()
            if user_answer is None:
                return

            if quiz.is_correct(user_answer):
                print("정답입니다!")
                correct_count += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {correct_count}/{total}")
        if correct_count > self.best_score:
            self.best_score = correct_count
            print(f"최고 점수를 갱신했습니다: {self.best_score}")
        else:
            print(f"최고 점수는 {self.best_score}입니다.")
        self.save_state()

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
