import unittest
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


if __name__ == "__main__":
    unittest.main()
