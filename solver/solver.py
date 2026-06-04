# Main solver logic utilizing entropy.py for calculations
from solver.entropy import compute_entropy, unresolved_check
from game.state import Guess

SIMILAR_LIMIT = 6   # Switch to check unresolved letters when candidates drop to this value
ENTROPY_DIFF = 0.25 # Words within an entropy difference of this value of the best are treated as tied

class Solver:
    def __init__(self, state, all_words: list[str]):
        self.state = state
        self.all_words = all_words  # Full word list, not just remaining candidates

    # Returns next best guess based on entropy scoring.
    # For small candidate sets, uses unresolved letter analysis as a tiebreaker
    # among words with similar entropy to avoid wasted guesses.
    def next_guess(self) -> str:
        candidates = self.state.candidates
        word_scores = []

        if len(candidates) == 1:
            return candidates[0]

        if len(self.state.past_guesses) == 0:
            return self.state.starter

        # Score every word against remaining candidates and sort by entropy
        for w in self.all_words:
            word_scores.append((compute_entropy(w, candidates), w))
        word_scores.sort(reverse = True)

        best_entropy = word_scores[0][0]

        # If number of candidates left reaches predefined limit, entropy differences reach
        # defined value so use unresolved check to break ties and avoid wasting a guess
        if len(candidates) <= SIMILAR_LIMIT:
            top_words = []
            best_word = None
            best_score = -1

            for e, w in word_scores:
                if e >= best_entropy - ENTROPY_DIFF:
                    top_words.append(w)

            for w in top_words:
                score = unresolved_check(w, candidates, self.state)
                if score > best_score:
                    best_score = score
                    best_word = w

            return best_word

        return word_scores[0][1]


    # Makes the guess and updates variables
    def make_guess(self, guess_word: str, hints: str) -> None:
        past_candidates_count = len(self.state.candidates)
        entropy = compute_entropy(guess_word, self.state.candidates)
        guess = Guess(guess_word, hints, entropy, past_candidates_count)
        self.state.add_guess(guess)
