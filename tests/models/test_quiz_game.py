import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.models.quiz import Quiz
from src.models.quiz_game import QuizGame


class TestQuizGame(unittest.TestCase):
    def test_play_quiz_handles_empty_quizzes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = []
            with patch("builtins.print") as print_mock:
                game.play_quiz()
            print_mock.assert_any_call("출제할 퀴즈가 없습니다.")

    def test_play_quiz_retries_invalid_answer_and_scores(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("Q1", ["a", "b", "c", "d"], 2),
                Quiz("Q2", ["a", "b", "c", "d"], 1),
            ]
            with patch("builtins.input", side_effect=["", "abc", "5", "2", "1"]):
                game.play_quiz()

            self.assertEqual(game.best_score, 2)

    def test_play_quiz_saves_state_after_round(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            game.quizzes = [Quiz("Q1", ["a", "b", "c", "d"], 1)]
            with patch("builtins.input", side_effect=["1"]):
                game.play_quiz()
            self.assertTrue(state_path.exists())

            reloaded = QuizGame(state_file_path=state_path)
            self.assertEqual(reloaded.best_score, 1)

    def test_play_quiz_handles_keyboard_interrupt_safely(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [Quiz("Q1", ["a", "b", "c", "d"], 1)]
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                game.play_quiz()
            self.assertFalse(game._is_running)

    def test_menu_choice_one_dispatches_play_quiz(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            with patch.object(game, "play_quiz") as play_quiz_mock:
                game._dispatch_menu(1)
            play_quiz_mock.assert_called_once()

    def test_add_quiz_adds_new_item_and_saves(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            initial_count = len(game.quizzes)
            with patch(
                "builtins.input",
                side_effect=["새 문제", "선택1", "선택2", "선택3", "선택4", "2", "힌트"],
            ):
                game.add_quiz()

            self.assertEqual(len(game.quizzes), initial_count + 1)
            self.assertTrue(state_path.exists())

            reloaded = QuizGame(state_file_path=state_path)
            self.assertTrue(any(q.question == "새 문제" for q in reloaded.quizzes))

    def test_add_quiz_retries_invalid_answer_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            with patch(
                "builtins.input",
                side_effect=[
                    "문제",
                    "a",
                    "b",
                    "c",
                    "d",
                    "",
                    "abc",
                    "9",
                    "1",
                    "",
                ],
            ):
                game.add_quiz()

            self.assertTrue(any(q.question == "문제" and q.answer == 1 for q in game.quizzes))

    def test_add_quiz_interrupt_keeps_data_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            initial_count = len(game.quizzes)
            with patch("builtins.input", side_effect=["문제", KeyboardInterrupt]):
                game.add_quiz()

            self.assertEqual(len(game.quizzes), initial_count)
            self.assertFalse(game._is_running)


if __name__ == "__main__":
    unittest.main()
