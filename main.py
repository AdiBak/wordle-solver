import random
from pathlib import Path

from utils.wordleDB import WordleDB
from game.state import GameState
from game.controller import GameController
from solver.solver import Solver
from utils.wordleUI import WordleUI

STARTER = "raise"
MAX_ATTEMPTS = 6
WORD_LENGTH = 5

# Loads the word list, picks a random target, and runs the auto solver.
def main() -> None:
    words_path = Path(__file__).parent / "utils" / "words.txt"
    db = WordleDB(words_path)
    words = db.get_words()
    target = random.choice(words)

    state = GameState(
        target = target,
        max_attempts = MAX_ATTEMPTS,
        length = WORD_LENGTH,
        candidates = list(words),
        starter = STARTER,
    )
    ui = WordleUI()
    solver = Solver(state)
    controller = GameController(state, solver, ui)

    controller.run()


if __name__ == "__main__":
    main()
