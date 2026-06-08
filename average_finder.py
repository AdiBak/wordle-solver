from main import run_one_game

# change depending on which file you use and how many games you want to run and how many games
NUM_GAMES = 100

def main():
    total_guesses = 0
    solved_count = 0

    for i in range(NUM_GAMES):
        result = run_one_game()
        total_guesses += result.num_guesses()

        if result.solved:
            solved_count += 1
    
    average = total_guesses / NUM_GAMES

    print(f"# of games: {NUM_GAMES}")
    print(f"# solved: {solved_count}")
    print(f"Average guesses per game: {average}")

if __name__ == "__main__":
    main()
