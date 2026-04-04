from src.models.quiz import Quiz


def build_default_quizzes() -> list[Quiz]:
    """Return the default Python basics quiz set."""
    return [
        Quiz(
            question="파이썬에서 정수형 타입은 무엇인가요?",
            choices=["str", "int", "list", "dict"],
            answer=2,
            hint="숫자를 그대로 다루는 기본 내장 타입을 떠올려보세요.",
        ),
        Quiz(
            question="조건에 따라 분기할 때 사용하는 키워드 조합은 무엇인가요?",
            choices=["for / while", "def / return", "if / elif / else", "try / except / finally"],
            answer=3,
            hint="조건문은 보통 if로 시작하고, 추가 분기는 elif를 사용합니다.",
        ),
        Quiz(
            question="리스트의 길이를 구할 때 사용하는 함수는 무엇인가요?",
            choices=["size()", "count()", "len()", "length()"],
            answer=3,
            hint="문자열과 리스트 같은 컬렉션의 길이를 잴 때 쓰는 내장 함수를 떠올려보세요.",
        ),
        Quiz(
            question="함수를 정의할 때 사용하는 키워드는 무엇인가요?",
            choices=["class", "def", "func", "lambda"],
            answer=2,
            hint="파이썬에서 함수 선언은 세 글자 키워드로 시작합니다.",
        ),
        Quiz(
            question="클래스의 생성자 역할을 하는 특수 메서드는 무엇인가요?",
            choices=["__new__", "__init__", "__main__", "__class__"],
            answer=2,
            hint="인스턴스가 만들어진 직후 초기화를 담당하는 메서드입니다.",
        ),
    ]
