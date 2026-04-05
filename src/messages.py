"""앱 전역 사용자 안내 및 검증 오류 메시지(단일 출처)."""

# --- 터미널 입력 UX (QuizGame) ---

MSG_EMPTY_INPUT = "입력을 확인해주세요. 비어 있는 값은 사용할 수 없습니다."
MSG_NOT_AN_INTEGER = "숫자로 입력해주세요."
MSG_NUMBER_OR_HINT = "숫자 또는 h로 입력해주세요."
MSG_HINT_ALREADY_USED = "힌트는 한 번만 볼 수 있습니다."


def format_menu_range_error(lo: int, hi: int) -> str:
    return f"{lo}에서 {hi} 사이 숫자를 입력해주세요."


# --- 상태 파일 ---

MSG_INVALID_STATE_SCHEMA = "상태 데이터 형식이 올바르지 않습니다."
MSG_STATE_RECOVER = "상태 파일을 읽을 수 없어 기본 데이터로 복구합니다."
MSG_QUIZ_CREATE_FAILED = "퀴즈를 저장할 수 없습니다. 입력을 확인해 주세요."


# --- Quiz 모델 ValueError ---

QUIZ_QUESTION_NOT_STR = "문제는 문자열이어야 합니다."
QUIZ_HINT_NOT_STR = "힌트는 문자열이어야 합니다."
QUIZ_CHOICE_NOT_STR = "각 선택지는 문자열이어야 합니다."
QUIZ_QUESTION_EMPTY = "문제는 비어 있을 수 없습니다."
QUIZ_CHOICES_NOT_LIST = "선택지는 목록 형식이어야 합니다."
QUIZ_CHOICES_COUNT_FOUR = "선택지는 정확히 4개여야 합니다."
QUIZ_CHOICE_ITEM_EMPTY = "각 선택지는 비어 있을 수 없습니다."
QUIZ_ANSWER_NOT_INT = "정답 번호는 정수여야 합니다."
QUIZ_HINT_EMPTY = "힌트는 비어 있을 수 없습니다."
QUIZ_FROM_DICT_NOT_DICT = "문항 데이터는 딕셔너리 형식이어야 합니다."
