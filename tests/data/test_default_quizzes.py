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

    def test_build_default_quizzes_contains_python_basics_topics(self) -> None:
        # 기본 퀴즈 세트가 의도한 파이썬 기초 주제들을 포함하는지 확인한다.
        quizzes = build_default_quizzes()
        questions = {quiz.question for quiz in quizzes}
        expected_questions = {
            "파이썬에서 정수형 타입은 무엇인가요?",
            "조건에 따라 분기할 때 사용하는 키워드 조합은 무엇인가요?",
            "리스트의 길이를 구할 때 사용하는 함수는 무엇인가요?",
            "함수를 정의할 때 사용하는 키워드는 무엇인가요?",
            "클래스의 생성자 역할을 하는 특수 메서드는 무엇인가요?",
        }

        self.assertTrue(expected_questions.issubset(questions))


if __name__ == "__main__":
    unittest.main()
