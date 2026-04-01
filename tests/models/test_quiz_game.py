import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.models.quiz_game import QuizGame


class TestQuizGameMenuSkeleton(unittest.TestCase):
    def test_get_menu_choice_retries_until_valid_number(self) -> None:
        game = QuizGame()
        with patch("builtins.input", side_effect=[" ", "abc", "9", "2"]):
            choice = game.get_menu_choice()
        self.assertEqual(choice, 2)

    def test_run_stops_on_exit_menu(self) -> None:
        game = QuizGame()
        with patch("builtins.input", side_effect=["5"]):
            game.run()
        self.assertFalse(game._is_running)

    def test_get_menu_choice_handles_keyboard_interrupt_safely(self) -> None:
        game = QuizGame()
        with patch("builtins.input", side_effect=KeyboardInterrupt), patch.object(
            game, "save_state"
        ) as save_state_mock:
            choice = game.get_menu_choice()
        self.assertIsNone(choice)
        self.assertFalse(game._is_running)
        save_state_mock.assert_called_once()

    def test_get_menu_choice_handles_eoferror_safely(self) -> None:
        game = QuizGame()
        with patch("builtins.input", side_effect=EOFError), patch.object(
            game, "save_state"
        ) as save_state_mock:
            choice = game.get_menu_choice()
        self.assertIsNone(choice)
        self.assertFalse(game._is_running)
        save_state_mock.assert_called_once()

    def test_safe_shutdown_still_stops_when_save_fails(self) -> None:
        game = QuizGame()
        with patch.object(game, "save_state", side_effect=RuntimeError("save failed")):
            game._handle_safe_shutdown()
        self.assertFalse(game._is_running)

    def test_load_state_uses_defaults_when_file_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            self.assertFalse(state_path.exists())
            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertEqual(game.best_score, 0)

    def test_save_and_load_state_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            game.best_score = 3
            game.save_state()

            reloaded = QuizGame(state_file_path=state_path)
            self.assertEqual(reloaded.best_score, 3)
            self.assertEqual(len(reloaded.quizzes), len(game.quizzes))
            self.assertEqual(reloaded.quizzes[0].question, game.quizzes[0].question)

    def test_load_state_fallback_when_json_is_corrupted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            state_path.write_text("{ this is not json", encoding="utf-8")
            game = QuizGame(state_file_path=state_path)
            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertEqual(game.best_score, 0)

    def test_load_state_fallback_when_schema_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            state_path.write_text(json.dumps({"best_score": "x"}), encoding="utf-8")
            game = QuizGame(state_file_path=state_path)
            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertEqual(game.best_score, 0)


if __name__ == "__main__":
    unittest.main()
