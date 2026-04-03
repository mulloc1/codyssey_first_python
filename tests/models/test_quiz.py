import unittest

from src.models.quiz import Quiz


class TestQuizValidation(unittest.TestCase):
    def test_init_raises_attribute_error_when_question_is_not_string(self) -> None:
        # question이 문자열이 아니면 strip 호출 단계에서 AttributeError가 발생한다.
        with self.assertRaises(AttributeError):
            Quiz(123, ["a", "b", "c", "d"], 1)  # type: ignore[arg-type]

    def test_init_rejects_empty_question(self) -> None:
        # question이 공백/빈 문자열이면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("   ", ["a", "b", "c", "d"], 1)

        self.assertEqual(str(context.exception), "question must not be empty")

    def test_init_rejects_non_list_choices(self) -> None:
        # choices가 list 타입이 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", "a,b,c,d", 1)  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), "choices must be a list")

    def test_init_rejects_choices_length_not_four(self) -> None:
        # choices 길이가 4가 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c"], 1)

        self.assertEqual(str(context.exception), "choices must contain exactly 4 items")

    def test_init_rejects_empty_choice_item(self) -> None:
        # choices 항목 중 공백/빈 문자열이 있으면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", " ", "c", "d"], 1)

        self.assertEqual(str(context.exception), "choice must not be empty")

    def test_init_raises_attribute_error_when_choice_item_is_not_string(self) -> None:
        # choices 항목이 문자열이 아니면 strip 호출 단계에서 AttributeError가 발생한다.
        with self.assertRaises(AttributeError):
            Quiz("문제", ["a", 2, "c", "d"], 1)  # type: ignore[list-item]

    def test_init_rejects_non_integer_answer(self) -> None:
        # answer가 정수가 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c", "d"], "1")  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), "answer must be an integer")

    def test_init_rejects_out_of_range_answer(self) -> None:
        # answer가 1..4 범위를 벗어나면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz("문제", ["a", "b", "c", "d"], 5)

        self.assertEqual(str(context.exception), "answer must be in range 1..4")

    def test_init_normalizes_question_choices_and_hint(self) -> None:
        # 유효한 입력이면 문자열 필드가 trim 되어 저장되어야 한다.
        quiz = Quiz(
            question="  파이썬 문제  ",
            choices=[" a ", "b ", " c", "d"],
            answer=2,
        )

        self.assertEqual(quiz.question, "파이썬 문제")
        self.assertEqual(quiz.choices, ["a", "b", "c", "d"])
        self.assertEqual(quiz.answer, 2)


class TestQuizFromDict(unittest.TestCase):
    def test_from_dict_rejects_non_dictionary_input(self) -> None:
        # from_dict 입력이 dict가 아니면 예외가 발생해야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz.from_dict([])  # type: ignore[arg-type]

        self.assertEqual(str(context.exception), "data must be a dictionary")

    def test_from_dict_creates_quiz_from_valid_data(self) -> None:
        # 유효한 dict 데이터로 Quiz 객체가 생성되어야 한다.
        quiz = Quiz.from_dict(
            {
                "question": "  문제  ",
                "choices": [" a ", "b", "c", "d "],
                "answer": 3,
            }
        )

        self.assertEqual(quiz.question, "문제")
        self.assertEqual(quiz.choices, ["a", "b", "c", "d"])
        self.assertEqual(quiz.answer, 3)

    def test_from_dict_propagates_constructor_validation_error(self) -> None:
        # dict 값이 잘못되면 생성자 검증 예외가 그대로 전달되어야 한다.
        with self.assertRaises(ValueError) as context:
            Quiz.from_dict(
                {
                    "question": "문제",
                    "choices": ["a", "b", "c", "d"],
                    "answer": 9,
                }
            )

        self.assertEqual(str(context.exception), "answer must be in range 1..4")

    def test_from_dict_raises_key_error_when_required_field_is_missing(self) -> None:
        # 필수 키가 누락된 dict는 현재 구현 기준으로 KeyError가 발생한다.
        with self.assertRaises(KeyError):
            Quiz.from_dict(
                {
                    "choices": ["a", "b", "c", "d"],
                    "answer": 1,
                }
            )


if __name__ == "__main__":
    unittest.main()
