class Quiz:
    """Model that represents one multiple-choice quiz item."""

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str | None = None,
    ) -> None:
        # question 공백 제거
        question_clean = question.strip()
        if not question_clean:
            raise ValueError("question must not be empty")

        # choices 타입 검증
        # JSON 로드 데이터는 신뢰할 수 없으므로 choices 타입/구조를 검증한다.
        if not isinstance(choices, list):
            raise ValueError("choices must be a list")

        # 선택지 갯수 검증
        if len(choices) != 4:
            raise ValueError("choices must contain exactly 4 items")

        # 각 선택지 별로 공백 제거
        normalized_choices: list[str] = []
        for choice in choices:
            choice_clean = choice.strip()
            if not choice_clean:
                raise ValueError("choice must not be empty")
            normalized_choices.append(choice_clean)


        # answer 타입 및 범위 검증
        # JSON 로드 데이터는 신뢰할 수 없으므로 answer 타입/범위를 검증한다.
        if not isinstance(answer, int):
            raise ValueError("answer must be an integer")

        # 정답 범위 검증
        if answer < 1 or answer > 4:
            raise ValueError("answer must be in range 1..4")

        # hint 타입 검증
        # JSON 로드 데이터는 신뢰할 수 없으므로 hint 타입을 검증한다.
        if hint is not None and not isinstance(hint, str):
            raise ValueError("hint must be a string or None")

        self.question = question_clean
        self.choices = normalized_choices
        self.answer = answer
        self.hint = hint.strip() if isinstance(hint, str) else None

    # 질문들의 출력 형태를 만들어 리턴하는 메서드
    def format_question(self) -> str:
        lines = [self.question]
        for idx, choice in enumerate(self.choices, start=1):
            lines.append(f"{idx}. {choice}")
        return "\n".join(lines)

    # 정답이 맞는 지 확인하는 메서드
    def is_correct(self, user_answer: int) -> bool:
        if not isinstance(user_answer, int):
            return False
        return user_answer == self.answer

    # 객체를 딕셔너리로 변환하는 메서드
    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    # 딕셔너리를 객체로 변환하는 클래스 메서드
    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint"),
        )
