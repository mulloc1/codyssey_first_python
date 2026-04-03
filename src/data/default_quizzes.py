from src.models.quiz import Quiz


def build_default_quizzes() -> list[Quiz]:
    """Return the default Python basics quiz set."""
    return [
        Quiz(
            question="파이썬에서 정수형 타입은 무엇인가요?",
            choices=["str", "int", "list", "dict"],
            answer=2,
        ),
        Quiz(
            question="조건에 따라 분기할 때 사용하는 키워드 조합은 무엇인가요?",
            choices=["for / while", "def / return", "if / elif / else", "try / except / finally"],
            answer=3,
        ),
        Quiz(
            question="리스트의 길이를 구할 때 사용하는 함수는 무엇인가요?",
            choices=["size()", "count()", "len()", "length()"],
            answer=3,
        ),
        Quiz(
            question="함수를 정의할 때 사용하는 키워드는 무엇인가요?",
            choices=["class", "def", "func", "lambda"],
            answer=2,
        ),
        Quiz(
            question="클래스의 생성자 역할을 하는 특수 메서드는 무엇인가요?",
            choices=["__new__", "__init__", "__main__", "__class__"],
            answer=2,
        ),
    ]
