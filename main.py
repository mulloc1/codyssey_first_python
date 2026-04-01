from src.models.quiz_game import QuizGame


def main() -> None:
    """Application entry point."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
