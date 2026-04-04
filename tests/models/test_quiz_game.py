import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from src.models.quiz import Quiz
from src.models.quiz_game import Menu, QuizGame


class TestQuizGame(unittest.TestCase):
    def test_play_quiz_handles_empty_quizzes(self) -> None:
        # 퀴즈가 하나도 없을 때 `play_quiz()`가 안내 메시지를 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = []
            with patch("builtins.print") as print_mock:
                game.play_quiz()
            print_mock.assert_any_call("출제할 퀴즈가 없습니다.")

    def test_play_quiz_retries_invalid_answer_and_scores(self) -> None:
        # 잘못된 입력을 반복적으로 무시하고, 정답 선택 시 최고 점수가 올바르게 갱신되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("Q1", ["a", "b", "c", "d"], 2, "Q1 힌트"),
                Quiz("Q2", ["a", "b", "c", "d"], 1, "Q2 힌트"),
            ]
            with (
                patch("src.models.quiz_game.random.shuffle", side_effect=lambda quizzes: None),
                patch("builtins.input", side_effect=["2", "", "abc", "5", "2", "1"]),
            ):
                game.play_quiz()

            self.assertEqual(game.best_score, 2)

    def test_play_quiz_saves_state_after_round(self) -> None:
        # 한 라운드가 끝난 뒤 상태(state)가 파일에 저장되고, 재로드 시 최고 점수가 유지되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            game.quizzes = [Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트")]
            with patch("builtins.input", side_effect=["1", "1"]):
                game.play_quiz()
            self.assertTrue(state_path.exists())

            reloaded = QuizGame(state_file_path=state_path)
            self.assertEqual(reloaded.best_score, 1)
            self.assertEqual(len(reloaded.history), 1)
            self.assertEqual(reloaded.history[0]["question_count"], 1)
            self.assertEqual(reloaded.history[0]["score"], 1)
            self.assertIsInstance(reloaded.history[0]["at"], str)

    def test_load_state_without_history_key_uses_empty_history(self) -> None:
        # state.json에 history 키가 없을 때 빈 기록으로 로드하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            quiz = Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트")
            payload = {"quizzes": [quiz.to_dict()], "best_score": 0}
            state_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            game = QuizGame(state_file_path=state_path)
            self.assertEqual(game.history, [])

    def test_load_state_invalid_history_entries_yield_empty_history(self) -> None:
        # history 항목 스키마가 잘못되면 기록만 비우고 퀴즈·최고 점수는 유지하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            quiz = Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트")
            payload = {
                "quizzes": [quiz.to_dict()],
                "best_score": 2,
                "history": [{"at": "x", "question_count": "bad", "score": 1}],
            }
            state_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            game = QuizGame(state_file_path=state_path)
            self.assertEqual(game.history, [])
            self.assertEqual(game.best_score, 2)
            self.assertEqual(len(game.quizzes), 1)

    def test_play_quiz_appends_history_with_fixed_timestamp(self) -> None:
        # 라운드 완료 시 history에 시각·문제 수·점수가 append되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("Q1", ["a", "b", "c", "d"], 2, "Q1 힌트"),
                Quiz("Q2", ["a", "b", "c", "d"], 1, "Q2 힌트"),
            ]
            fixed = datetime(2026, 4, 4, 14, 30, 0)
            with (
                patch("src.models.quiz_game.datetime") as dt_mock,
                patch("src.models.quiz_game.random.shuffle", side_effect=lambda quizzes: None),
                patch("builtins.input", side_effect=["2", "2", "1"]),
            ):
                dt_mock.now.return_value = fixed
                game.play_quiz()

            self.assertEqual(len(game.history), 1)
            self.assertEqual(
                game.history[0],
                {
                    "at": "2026-04-04T14:30:00",
                    "question_count": 2,
                    "score": 2,
                },
            )

    def test_play_quiz_handles_keyboard_interrupt_safely(self) -> None:
        # `KeyboardInterrupt`가 발생해도 게임 상태 플래그(`_is_running`)가 안전하게 꺼지는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트")]
            with patch("builtins.input", side_effect=["1", KeyboardInterrupt]):
                game.play_quiz()
            self.assertFalse(game._is_running)

    def test_play_quiz_uses_shuffled_order_without_mutating_source(self) -> None:
        # 출제 시에는 셔플된 순서를 따르되, 원본 퀴즈 목록 순서는 유지되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트"),
                Quiz("Q2", ["a", "b", "c", "d"], 1, "Q2 힌트"),
            ]

            def reverse_quizzes(quizzes: list[Quiz]) -> None:
                quizzes.reverse()

            with (
                patch("src.models.quiz_game.random.shuffle", side_effect=reverse_quizzes),
                patch("builtins.input", side_effect=["2", "1", "1"]),
                patch("builtins.print") as print_mock,
            ):
                game.play_quiz()

            printed_questions = [
                args[0]
                for args, _ in print_mock.call_args_list
                if args and isinstance(args[0], str) and args[0].startswith("Q")
            ]
            self.assertEqual(
                printed_questions[:2],
                [game.quizzes[1].format_question(), game.quizzes[0].format_question()],
            )
            self.assertEqual([quiz.question for quiz in game.quizzes], ["Q1", "Q2"])

    def test_play_quiz_shows_hint_and_deducts_score(self) -> None:
        # 힌트를 본 뒤 정답을 맞히면 정답 수는 올라가지만 점수는 차감되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [Quiz("Q1", ["a", "b", "c", "d"], 1, "정답은 숫자 타입입니다.")]

            with (
                patch("src.models.quiz_game.random.shuffle", side_effect=lambda quizzes: None),
                patch("builtins.input", side_effect=["1", "h", "1"]),
                patch("builtins.print") as print_mock,
            ):
                game.play_quiz()

            print_mock.assert_any_call("힌트: 정답은 숫자 타입입니다.")
            print_mock.assert_any_call("힌트를 사용하여 이 문제 점수는 0점입니다.")
            print_mock.assert_any_call("이번 점수: 0/1")
            self.assertEqual(game.best_score, 0)

    def test_play_quiz_retries_invalid_question_count_input(self) -> None:
        # 문제 수 입력이 유효하지 않으면 재입력을 요구하고, 유효한 값 이후 정상 진행하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트"),
                Quiz("Q2", ["a", "b", "c", "d"], 1, "Q2 힌트"),
            ]
            with (
                patch("builtins.input", side_effect=["", "abc", "3", "1", "1"]),
                patch("builtins.print") as print_mock,
            ):
                game.play_quiz()

            print_mock.assert_any_call("입력을 확인해주세요. 비어 있는 값은 사용할 수 없습니다.")
            print_mock.assert_any_call("숫자로 입력해주세요.")
            print_mock.assert_any_call("1에서 2 사이 숫자를 입력해주세요.")
            self.assertEqual(game.best_score, 1)

    def test_play_quiz_handles_question_count_interrupt_safely(self) -> None:
        # 문제 수 입력 단계에서 인터럽트가 발생해도 안전 종료 플래그가 꺼지는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트")]
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                game.play_quiz()
            self.assertFalse(game._is_running)

    def test_play_quiz_uses_selected_count_from_shuffled_quizzes(self) -> None:
        # 셔플된 목록에서 선택한 문제 수만큼만 출제하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("Q1", ["a", "b", "c", "d"], 1, "Q1 힌트"),
                Quiz("Q2", ["a", "b", "c", "d"], 1, "Q2 힌트"),
                Quiz("Q3", ["a", "b", "c", "d"], 1, "Q3 힌트"),
            ]

            def reverse_quizzes(quizzes: list[Quiz]) -> None:
                quizzes.reverse()

            with (
                patch("src.models.quiz_game.random.shuffle", side_effect=reverse_quizzes),
                patch("builtins.input", side_effect=["2", "1", "1"]),
                patch("builtins.print") as print_mock,
            ):
                game.play_quiz()

            printed_questions = [
                args[0]
                for args, _ in print_mock.call_args_list
                if args and isinstance(args[0], str) and args[0].startswith("Q")
            ]
            self.assertEqual(
                printed_questions[:2],
                [game.quizzes[2].format_question(), game.quizzes[1].format_question()],
            )
            self.assertNotIn(game.quizzes[0].format_question(), printed_questions[:2])

    def test_menu_choice_one_dispatches_play_quiz(self) -> None:
        # 메뉴 선택 1이 내부적으로 `play_quiz()`를 호출하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            with patch.object(game, "play_quiz") as play_quiz_mock:
                game._dispatch_menu(Menu.PLAY)
            play_quiz_mock.assert_called_once()

    def test_add_quiz_adds_new_item_and_saves(self) -> None:
        # `add_quiz()`가 새 퀴즈를 추가하고 상태 파일에 저장하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            initial_count = len(game.quizzes)
            with patch(
                "builtins.input",
                side_effect=["새 문제", "선택1", "선택2", "선택3", "선택4", "새 힌트", "2"],
            ):
                game.add_quiz()

            self.assertEqual(len(game.quizzes), initial_count + 1)
            self.assertTrue(state_path.exists())

            reloaded = QuizGame(state_file_path=state_path)
            self.assertTrue(any(q.question == "새 문제" and q.hint == "새 힌트" for q in reloaded.quizzes))

    def test_add_quiz_retries_invalid_answer_input(self) -> None:
        # 정답 입력이 유효하지 않을 때 `add_quiz()`가 재입력을 요구하며, 최종적으로 정답이 정상 반영되는지 확인한다.
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
                    "힌트",
                    "",
                    "abc",
                    "9",
                    "1",
                ],
            ):
                game.add_quiz()

            self.assertTrue(any(q.question == "문제" and q.answer == 1 and q.hint == "힌트" for q in game.quizzes))

    def test_add_quiz_interrupt_keeps_data_unchanged(self) -> None:
        # `add_quiz()` 도중 `KeyboardInterrupt`가 발생하면 퀴즈 목록이 변경되지 않는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            initial_count = len(game.quizzes)
            with patch("builtins.input", side_effect=["문제", KeyboardInterrupt]):
                game.add_quiz()

            self.assertEqual(len(game.quizzes), initial_count)
            self.assertFalse(game._is_running)

    def test_menu_choice_three_dispatches_list_quizzes(self) -> None:
        # 메뉴 선택 3이 내부적으로 `list_quizzes()`를 호출하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            with patch.object(game, "list_quizzes") as list_quizzes_mock:
                game._dispatch_menu(Menu.LIST)
            list_quizzes_mock.assert_called_once()

    def test_list_quizzes_handles_empty_list(self) -> None:
        # 등록된 퀴즈가 없을 때 `list_quizzes()`가 안내 메시지를 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = []
            with patch("builtins.print") as print_mock:
                game.list_quizzes()
            print_mock.assert_any_call("등록된 퀴즈가 없습니다.")

    def test_list_quizzes_prints_numbered_questions(self) -> None:
        # `list_quizzes()`가 문제를 번호와 함께 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("문제A", ["a", "b", "c", "d"], 1, "문제A 힌트"),
                Quiz("문제B", ["a", "b", "c", "d"], 2, "문제B 힌트"),
            ]
            with patch("builtins.print") as print_mock:
                game.list_quizzes()

            print_mock.assert_any_call("\n=== 퀴즈 목록 ===")
            print_mock.assert_any_call("1. 문제A")
            print_mock.assert_any_call("2. 문제B")

    def test_list_quizzes_reflects_added_quiz(self) -> None:
        # 퀴즈를 추가한 뒤 재로드하여 `list_quizzes()` 출력에 반영되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            with patch(
                "builtins.input",
                side_effect=["목록 확인 문제", "a", "b", "c", "d", "목록 힌트", "1"],
            ):
                game.add_quiz()

            reloaded = QuizGame(state_file_path=state_path)
            with patch("builtins.print") as print_mock:
                reloaded.list_quizzes()
            print_mock.assert_any_call(f"{len(reloaded.quizzes)}. 목록 확인 문제")

    def test_menu_choice_four_dispatches_show_best_score(self) -> None:
        # 메뉴 선택 4가 내부적으로 `show_best_score()`를 호출하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            with patch.object(game, "show_best_score") as show_best_score_mock:
                game._dispatch_menu(Menu.SCORE)
            show_best_score_mock.assert_called_once()

    def test_menu_choice_five_dispatches_delete_quiz(self) -> None:
        # 메뉴 선택 5가 내부적으로 `delete_quiz()`를 호출하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            with patch.object(game, "delete_quiz") as delete_quiz_mock:
                game._dispatch_menu(Menu.DELETE)
            delete_quiz_mock.assert_called_once()

    def test_delete_quiz_handles_empty_list(self) -> None:
        # 퀴즈가 없을 때 삭제 진입 시 안내 메시지만 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = []
            with patch("builtins.print") as print_mock:
                game.delete_quiz()
            print_mock.assert_any_call("삭제할 퀴즈가 없습니다.")

    def test_delete_quiz_removes_item_and_saves_state(self) -> None:
        # 유효한 번호로 삭제하면 목록이 줄고 상태 파일에 반영되는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            game = QuizGame(state_file_path=state_path)
            game.quizzes = [
                Quiz("A", ["a", "b", "c", "d"], 1, "hA"),
                Quiz("B", ["a", "b", "c", "d"], 2, "hB"),
            ]
            with patch("builtins.input", side_effect=["1"]):
                game.delete_quiz()

            self.assertEqual(len(game.quizzes), 1)
            self.assertEqual(game.quizzes[0].question, "B")
            reloaded = QuizGame(state_file_path=state_path)
            self.assertEqual(len(reloaded.quizzes), 1)
            self.assertEqual(reloaded.quizzes[0].question, "B")

    def test_delete_quiz_retries_invalid_index_input(self) -> None:
        # 삭제 번호 입력이 잘못되면 재입력을 요구하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [
                Quiz("A", ["a", "b", "c", "d"], 1, "hA"),
                Quiz("B", ["a", "b", "c", "d"], 2, "hB"),
            ]
            with patch("builtins.input", side_effect=["", "abc", "9", "2"]):
                game.delete_quiz()

            self.assertEqual(len(game.quizzes), 1)
            self.assertEqual(game.quizzes[0].question, "A")

    def test_delete_quiz_handles_keyboard_interrupt_safely(self) -> None:
        # 삭제 번호 입력 중 인터럽트가 발생하면 안전 종료 플래그가 꺼지는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.quizzes = [Quiz("A", ["a", "b", "c", "d"], 1, "hA")]
            initial_count = len(game.quizzes)
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                game.delete_quiz()

            self.assertEqual(len(game.quizzes), initial_count)
            self.assertFalse(game._is_running)

    def test_show_best_score_when_no_play_history(self) -> None:
        # 플레이 기록이 없을 때 최고 점수와 안내 문구를 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.best_score = 0
            game.history = []
            with patch("builtins.print") as print_mock:
                game.show_best_score()
            print_mock.assert_any_call("현재 최고 점수: 0")
            print_mock.assert_any_call("저장된 플레이 기록이 없습니다.")

    def test_show_best_score_when_score_exists(self) -> None:
        # 최고 점수가 존재할 때 `show_best_score()`가 현재 최고 점수를 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.best_score = 3
            game.history = []
            with patch("builtins.print") as print_mock:
                game.show_best_score()
            print_mock.assert_any_call("현재 최고 점수: 3")
            print_mock.assert_any_call("저장된 플레이 기록이 없습니다.")

    def test_show_best_score_prints_history_newest_first(self) -> None:
        # 플레이 기록이 있으면 최신순으로 목록을 출력하는지 확인한다.
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame(state_file_path=Path(temp_dir) / "state.json")
            game.best_score = 2
            game.history = [
                {"at": "2026-01-01T10:00:00", "question_count": 2, "score": 1},
                {"at": "2026-01-02T10:00:00", "question_count": 2, "score": 2},
            ]
            with patch("builtins.print") as print_mock:
                game.show_best_score()
            print_mock.assert_any_call("현재 최고 점수: 2")
            print_mock.assert_any_call("\n=== 플레이 기록 (최신순) ===")
            print_mock.assert_any_call("1. 2026-01-02T10:00:00 | 문제 2개 | 점수 2/2")
            print_mock.assert_any_call("2. 2026-01-01T10:00:00 | 문제 2개 | 점수 1/2")


if __name__ == "__main__":
    unittest.main()
