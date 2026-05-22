# Represents a single guess made by the player in the game.
class Guess:
    def __init__(self, word: str, hints: str, entropy: float = 0.0, past_candidates_count: int = 0):
        self.word = word # Guessed word
        self.hints = hints # String of hints indicating correctness of each letter in the guess (G, Y, N)
        self.entropy = entropy # Entropy value representing the information gain from making this guess
        self.past_candidates_count = past_candidates_count # Number of candidate words remaining before this guess


    # Returns whether the guess is a winning guess (all letters are correct).
    def is_win(self) -> bool:
        return self.hints == "GGGGG"


    # Returns the number of green hints (correct letters in the correct position) in the guess.
    def get_green_count(self) -> int:
        return self.hints.count("G")


    # Returns the number of yellow hints (correct letters in the wrong position) in the guess.
    def get_yellow_count(self) -> int:
        return self.hints.count("Y")


    # Returns the assigned entropy value for the guess, which represents the information 
    # gain from making that guess.
    def get_entropy(self) -> float:
        return self.entropy


    # Returns the number of candidate words remaining before this guess was made.
    def get_past_candidates(self) -> int:
        return self.past_candidates_count



# Represents the current state of the Wordle game.
class GameState:
    def __init__(self, target: str | None, max_attempts: int, length: int, candidates: list[str], starter: str):
        self.attempts: int = 0

        self.target: str | None = target # Target word
        self.max_attempts: int = max_attempts # Max number of attempts allowed per game (default: 6)
        self.length: int = length # Length of the target word (default: 5)
        self.candidates: list[str] = candidates # List of candidate words that can be guessed
        self.starter: str = starter # Starter word to use for the first guess
 
        self.past_guesses: list[Guess] = [] # List of past guesses made during the game, each represented as a Guess object object


    # Checks a word against the target word and returns a string of hints indicating which letters 
    # are correct (G), present but in the wrong position (Y), or not present (B). Deals with each character
    # positionally to ensure different combinations of letters are handled correctly.
    def check_word(guess: str, answer: str) -> str:
        result = ["B"] * 5
        pool = list(answer)

        for i, (g, a) in enumerate(zip(guess, answer)):
            if g == a:
                result[i] = "G"
                pool[i] = None

        for i, g in enumerate(guess):
            if result[i] == "G":
                continue
            if g in pool:
                result[i] = "Y"
                pool[pool.index(g)] = None

        return "".join(result)


    # Returns the number of attempts made so far in the game.
    def get_attempts(self) -> int:
        return self.attempts
    

    # Returns whether the game has been solved (if the last guess was correct).
    def is_solved(self) -> bool:
        return bool(self.past_guesses) and self.past_guesses[-1].is_win()
    

    # Returns whether the game has ended (either solved or max attempts reached).
    def is_game_end(self) -> bool:
        return self.is_solved() or self.attempts >= self.max_attempts
    

    # Resets the game state to start a new game, optionally with a new target word and candidate list.
    def reset_board(self, target: str | None, candidates: list[str]) -> None:
        self.target = target
        self.candidates = candidates
        self.attempts = 0
        self.past_guesses = []
    

    # Adds a new guess to the game state, updating the list of past guesses and filtering the candidate 
    # list based on the hints received from the guess.
    def add_guess(self, guess: Guess) -> None:
        self.past_guesses.append(guess)
        self.attempts += 1

        if not guess.is_win():
            self.candidates = [c for c in self.candidates if GameState.check_word(guess.word, c) == guess.hints]


    # Prints the current game state information, including the target word, max attempts, 
    # length of the target word, number of candidates, starter word, and number of past guesses.
    def print_info(self):
        print(f"Target: {self.target}")
        print(f"Max Attempts: {self.max_attempts}")
        print(f"Length: {self.length}")
        print(f"Candidates: {len(self.candidates)}")
        print(f"Starter: {self.starter}")
        print(f"Past Guesses: {len(self.past_guesses)}")