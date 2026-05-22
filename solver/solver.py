# Main solver logic utilizing entropy.py for calculations
from solver.entropy import compute_entropy
from game.state import Guess

class Solver:
    def __init__(self, state):
        self.state = state
    
    # Returns next best guess based on entropy scoring
    def next_guess(self) -> str:
        candidates = self.state.candidates

        if len(self.state.past_guesses) == 0:
            return self.state.starter
        
        best_guess = None
        highest_entropy = -999

        for word in candidates:
            score = compute_entropy(word, candidates)

            if score > highest_entropy:
                best_guess = word
                highest_entropy = score

        return best_guess
    
    # Makes the guess and updates variables
    def make_guess(self, guess_word: str, hints: str) -> None:
        return
    
    