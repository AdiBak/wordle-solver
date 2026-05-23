from game.state import GameState, Guess
from game.controller import GameResult

# Terminal UI for the auto solver. Displays each guess with Wordle-style colors
# and prints a summary when the game ends.
class WordleUI:
    HINT_COLORS = {
        "G": "\033[42m\033[30m",  # green
        "Y": "\033[43m\033[30m",  # yellow
        "B": "\033[100m\033[37m", # gray
    }
    RESET = "\033[0m"

    # Called when a new game begins.
    def on_game_start(self, state: GameState) -> None:
        print()
        print("=" * 40)
        print("Wordle Auto Solver")
        print(f"Starter: {state.starter.upper()}")
        print(f"Candidates: {len(state.candidates)}")
        print("=" * 40)
        print()

    # Called after each guess is made.
    def on_turn(self, guess: Guess, state: GameState) -> None:
        attempt = state.get_attempts()
        row = self.format_guess(guess)
        remaining = len(state.candidates)

        print(f"Guess {attempt}/{state.max_attempts}: {row}")
        print(
            f"  entropy: {guess.get_entropy():.3f} | "
            f"candidates before: {guess.get_past_candidates()} | "
            f"candidates after: {remaining}"
        )
        print()

    # Called when the game ends.
    def on_game_end(self, result: GameResult) -> None:
        status = "SOLVED" if result.solved else "FAILED"

        print("=" * 40)
        print(f"[{status}] Target was {result.target.upper()}")
        print(f"Guesses used: {result.num_guesses()}")
        print()
        print("Board:")
        for guess in result.guesses:
            print(f"  {self.format_guess(guess)}")
        print("=" * 40)
        print()

    # Formats a single guess row with colored letter tiles.
    def format_guess(self, guess: Guess) -> str:
        tiles = []

        for letter, hint in zip(guess.word, guess.hints):
            color = self.HINT_COLORS[hint]
            tiles.append(f"{color} {letter.upper()} {self.RESET}")

        return " ".join(tiles)
