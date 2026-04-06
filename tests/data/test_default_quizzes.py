import unittest

from src.data.default_quizzes import build_default_quizzes
from src.models.quiz import Quiz


class TestDefaultQuizzes(unittest.TestCase):
    def test_build_default_quizzes_returns_quiz_instances(self) -> None:
        # 기본 퀴즈 빌더가 `Quiz` 인스턴스들의 리스트를 반환하는지 확인한다.
        quizzes = build_default_quizzes()

        self.assertIsInstance(quizzes, list)
        self.assertTrue(all(isinstance(quiz, Quiz) for quiz in quizzes))

    def test_build_default_quizzes_has_expected_minimum_count(self) -> None:
        # 기본 퀴즈가 최소 5개 이상 생성되는지 확인한다.
        quizzes = build_default_quizzes()

        self.assertGreaterEqual(len(quizzes), 5)

    def test_build_default_quizzes_has_unique_questions(self) -> None:
        # 기본 퀴즈 세트의 질문들이 중복 없이 구성되는지 확인한다.
        quizzes = build_default_quizzes()
        questions = [quiz.question for quiz in quizzes]

        self.assertEqual(len(questions), len(set(questions)))

    def test_build_default_quizzes_provide_non_empty_hints(self) -> None:
        # 기본 퀴즈는 모두 비어 있지 않은 힌트를 가져야 한다.
        quizzes = build_default_quizzes()

        self.assertTrue(all(isinstance(quiz.hint, str) and quiz.hint for quiz in quizzes))


if __name__ == "__main__":
    unittest.main()
