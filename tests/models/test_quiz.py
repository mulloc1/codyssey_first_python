import unittest

from src.messages import (
    QUIZ_CHOICE_ITEM_EMPTY,
    QUIZ_CHOICE_NOT_STR,
    QUIZ_CHOICES_COUNT_FOUR,
    QUIZ_CHOICES_NOT_LIST,
    QUIZ_FROM_DICT_NOT_DICT,
    QUIZ_HINT_EMPTY,
    QUIZ_HINT_NOT_STR,
    QUIZ_QUESTION_EMPTY,
    QUIZ_QUESTION_NOT_STR,
    QUIZ_ANSWER_NOT_INT,
    format_menu_range_error,
)
from src.models.quiz import Quiz


class TestQuizValidation(unittest.TestCase):
    def test_init_rejects_non_string_question(self) -> None:
        # question이 문자열이 아니면 ValueError가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz(123, ["a", "b", "c", "d"], 1, "힌트")  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), QUIZ_QUESTION_NOT_STR)

    def test_init_rejects_empty_question(self) -> None:
        # question이 공백/빈 문자열이면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("   ", ["a", "b", "c", "d"], 1, "힌트")

        self.assertEqual(str(context.exception), QUIZ_QUESTION_EMPTY)

    def test_init_rejects_non_list_choices(self) -> None:
        # choices가 list 타입이 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", "a,b,c,d", 1, "힌트")  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), QUIZ_CHOICES_NOT_LIST)

    def test_init_rejects_choices_length_not_four(self) -> None:
        # choices 길이가 4가 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c"], 1, "힌트")

        self.assertEqual(str(context.exception), QUIZ_CHOICES_COUNT_FOUR)

    def test_init_rejects_empty_choice_item(self) -> None:
        # choices 항목 중 공백/빈 문자열이 있으면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", " ", "c", "d"], 1, "힌트")

        self.assertEqual(str(context.exception), QUIZ_CHOICE_ITEM_EMPTY)

    def test_init_rejects_non_string_choice_item(self) -> None:
        # choices 항목이 문자열이 아니면 ValueError가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", 2, "c", "d"], 1, "힌트")  # type: ignore[list-item]

        self.assertEqual(str(context.exception), QUIZ_CHOICE_NOT_STR)

    def test_init_rejects_non_integer_answer(self) -> None:
        # answer가 정수가 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c", "d"], "1", "힌트")  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), QUIZ_ANSWER_NOT_INT)

    def test_init_rejects_out_of_range_answer(self) -> None:
        # answer가 1..4 범위를 벗어나면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c", "d"], 5, "힌트")

        self.assertEqual(str(context.exception), format_menu_range_error(1, 4))

    def test_init_rejects_empty_hint(self) -> None:
        # hint가 공백/빈 문자열이면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c", "d"], 1, "   ")

        self.assertEqual(str(context.exception), QUIZ_HINT_EMPTY)

    def test_init_rejects_non_string_hint(self) -> None:
        # hint가 문자열이 아니면 ValueError가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c", "d"], 1, 123)  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), QUIZ_HINT_NOT_STR)

    def test_init_normalizes_question_choices_and_hint(self) -> None:
        # 유효한 입력이면 문자열 필드가 trim 되어 저장되어야 한다.
        quiz = Quiz(
            question="  파이썬 문제  ",
            choices=[" a ", "b ", " c", "d"],
            answer=2,
            hint="  힌트 문장  ",
        )

        self.assertEqual(quiz.question, "파이썬 문제")
        self.assertEqual(quiz.choices, ["a", "b", "c", "d"])
        self.assertEqual(quiz.answer, 2)
        self.assertEqual(quiz.hint, "힌트 문장")


class TestQuizFromDict(unittest.TestCase):
    def test_from_dict_rejects_non_dictionary_input(self) -> None:
        # from_dict 입력이 dict가 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz.from_dict([])  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), QUIZ_FROM_DICT_NOT_DICT)

    def test_from_dict_creates_quiz_from_valid_data(self) -> None:
        # 유효한 dict 데이터로 Quiz 객체가 생성되어야 한다.
        quiz = Quiz.from_dict(
            {
                "question": "  문제  ",
                "choices": [" a ", "b", "c", "d "],
                "answer": 3,
                "hint": "  힌트  ",
            }
        )

        self.assertEqual(quiz.question, "문제")
        self.assertEqual(quiz.choices, ["a", "b", "c", "d"])
        self.assertEqual(quiz.answer, 3)
        self.assertEqual(quiz.hint, "힌트")

    def test_from_dict_propagates_constructor_validation_error(self) -> None:
        # dict 값이 잘못되면 생성자 검증 예외가 그대로 전달되어야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz.from_dict(
                {
                    "question": "문제",
                    "choices": ["a", "b", "c", "d"],
                    "answer": 9,
                    "hint": "힌트",
                }
            )

        self.assertEqual(str(context.exception), format_menu_range_error(1, 4))

    def test_from_dict_raises_key_error_when_required_field_is_missing(self) -> None:
        # 필수 키가 누락된 dict는 현재 구현 기준으로 KeyError가 발생한다.
        with self.assertRaises(KeyError):
            Quiz.from_dict(
                {
                    "choices": ["a", "b", "c", "d"],
                    "answer": 1,
                    "hint": "힌트",
                }
            )


if __name__ == "__main__":
    unittest.main()
