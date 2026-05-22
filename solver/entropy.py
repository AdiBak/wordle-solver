import math
from game.state import GameState

# For a given guess, score it against every remaining candidate to get a distribution of feedback patterns, 
# then compute entropy over that distribution.
# High entropy = guess splits candidates into many even groups = more information gained.
def compute_entropy(guess: str, candidates: list[str]) -> float:
    pattern_totals = {}
    entropy = 0.0
    total = len(candidates)

    for candidate in candidates:

        # Checks the guess against the candidate for a feedback pattern and
        # counts how many candidates produce each pattern.
        pattern = GameState.check_word(guess, candidate)
        pattern_totals[pattern] = pattern_totals.get(pattern, 0) + 1

    for count in pattern_totals.values():

        # Convert pattern counts into probabilities and compute entropy using formula
        p = count / total
        entropy -= p * math.log2(p)

    return entropy