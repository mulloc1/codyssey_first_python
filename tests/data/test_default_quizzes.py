import unittest

from src.data.default_quizzes import build_default_quizzes
from src.models.quiz import Quiz


class TestDefaultQuizzes(unittest.TestCase):
    def test_build_default_quizzes_returns_quiz_instances(self) -> None:
        quizzes = build_default_quizzes()

        self.assertIsInstance(quizzes, list)
        self.assertTrue(all(isinstance(quiz, Quiz) for quiz in quizzes))

    def test_build_default_quizzes_has_expected_minimum_count(self) -> None:
        quizzes = build_default_quizzes()

        self.assertGreaterEqual(len(quizzes), 5)

    def test_each_quiz_has_valid_domain_values(self) -> None:
        quizzes = build_default_quizzes()

        for quiz in quizzes:
            self.assertEqual(len(quiz.choices), 4)
            self.assertTrue(1 <= quiz.answer <= 4)
            self.assertTrue(bool(quiz.question.strip()))

    def test_each_quiz_choice_is_non_empty_string(self) -> None:
        quizzes = build_default_quizzes()

        for quiz in quizzes:
            for choice in quiz.choices:
                self.assertIsInstance(choice, str)
                self.assertTrue(bool(choice.strip()))


if __name__ == "__main__":
    unittest.main()
