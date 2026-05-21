from game.state import GameState, Guess

# Initializes a class to display game results for the user, 
# including whether the game was solved, the target word, and the list of guesses made.
class GameResult:
    def __init__(self, solved: bool, target: str, guesses: list[Guess]):
        self.solved = solved
        self.target = target
        self.guesses = guesses

    def num_guesses(self) -> int:
        return len(self.guesses)

    def __str__(self) -> str:
        status = "SOLVED" if self.solved else "FAILED"

        return (
            f"[{status}] | Target = {self.target}"
            f"Guesses: {self.num_guesses()} "
        )

# Main controller class that manages the game state, solver, and user interface. 
# It handles the main game loop and resetting the game if needed.
class GameController:
    def __init__(self, state: GameState, solver, ui) -> None:
        self.state = state # Current game state
        self.solver = solver # Entropy solver used to determine the best guess based on the current game state
        self.ui = ui # Links to user interface
        self.init_candidates = list(state.candidates) # Returns initial candidates list from database

    # Runs the main game loop, allowing the player to make guesses until the game is solved or 
    # the maximum number of attempts is reached.
    def run(self) -> GameResult:
        while not self.state.is_game_end():
            self.play_turn()

        result = GameResult(
            solved = self.state.is_solved(),
            target = self.state.target,
            guesses = list(self.state.past_guesses),
        )
        return result

    # TO DO: Handles a single turn of the game.
    def play_turn(self) -> None:
        return

    # TO DO: Resets the game state, solver, and user interface for a new game.
    def reset_game(self, target: str | None = None) -> None:
        return

    # Checks if the game has ended
    def check_end(self) -> bool:
        return self.state.is_game_end()
