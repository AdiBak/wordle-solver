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


# Returns how many positions in a word still have ambiguous letters across remaining candidates.
# Skips positions already confirmed green, counts positions where the letter appears in some but not all candidates.
# Used as a tiebreaker in solver.py when entropy scores are too close to make clear guesses.
def unresolved_check(word: str, candidates: list[str], state) -> int:
    score = 0
    n = len(candidates)
    green_positions = [False, False, False, False, False]

    # Collect positions already confirmed correct from past guesses
    for past_guess in state.past_guesses:
        for i, hint in enumerate(past_guess.hints):
            if hint == "G":
                green_positions[i] = True

    for i, letter in enumerate(word):\
        # Skip positions already confirmed green since provides no additional information gain
        if green_positions[i]:
            continue

        # Count how many candidates have this letter at this position
        matches = sum(1 for c in candidates if c[i] == letter)

        # Only considered good if splits candidates.
        # If all candidates or no candidates match the letter, less information gain so don't increment score
        if 0 < matches < n:
            score += 1

    return score