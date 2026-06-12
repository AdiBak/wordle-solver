import argparse
import csv
import random
from itertools import product
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt

from utils.wordleDB import WordleDB
from game.state import GameState
from game.controller import GameController
from solver.solver import Solver
import solver.solver as solver_mod
import main as main_mod

STARTER = "slate"
MAX_ATTEMPTS = 6
WORD_LENGTH = 5

def run_experiment(words: List[str], experiments: List[Tuple[int, float]], num_games: int = 20):
    results = []

    for similar_limit, entropy_diff in experiments:
        total_guesses = 0
        solved = 0

        solver_mod.SIMILAR_LIMIT = similar_limit
        solver_mod.ENTROPY_DIFF = entropy_diff

        for _ in range(num_games):
            result = main_mod.run_one_game()
            total_guesses += result.num_guesses()
            if result.solved:
                solved += 1

        average_guesses = total_guesses / num_games
        solved_ratio = solved / num_games
        results.append((similar_limit, entropy_diff, average_guesses, solved_ratio))
        print(
            f"SIMILAR_LIMIT={similar_limit}, ENTROPY_DIFF={entropy_diff:.2f} -> "
            f"solved={solved}/{num_games}, avg_guesses={average_guesses:.2f}"
        )

    return results


def save_results_csv(results: List[Tuple[int, float, float, float]], filename: str):
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["similar_limit", "entropy_diff", "average_guesses", "solve_ratio"])
        for similar_limit, entropy_diff, average_guesses, solved_ratio in results:
            writer.writerow([similar_limit, entropy_diff, average_guesses, solved_ratio])

    print(f"CSV saved to {filename}")


def plot_results(results: List[Tuple[int, float, float, float]], plot_file: str = "threshold_experiment_plot.png"):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

    entropy_diffs = sorted({entropy_diff for _, entropy_diff, _, _ in results})
    similar_limits = sorted({similar_limit for similar_limit, _, _, _ in results})

    for similar_limit in similar_limits:
        series = [
            next(avg for sim, diff, avg, _ in results if sim == similar_limit and diff == entropy_diff)
            for entropy_diff in entropy_diffs
        ]
        ax1.plot(entropy_diffs, series, marker="o", label=f"L={similar_limit}")

    for similar_limit in similar_limits:
        series = [
            next(ratio for sim, diff, _, ratio in results if sim == similar_limit and diff == entropy_diff)
            for entropy_diff in entropy_diffs
        ]
        ax2.plot(entropy_diffs, series, marker="s", label=f"L={similar_limit}")

    ax1.set_title("Average guesses by ENTROPY_DIFF for each SIMILAR_LIMIT")
    ax1.set_ylabel("Average guesses")
    ax1.legend(title="SIMILAR_LIMIT")
    ax1.grid(True)

    ax2.set_title("Solve ratio by ENTROPY_DIFF for each SIMILAR_LIMIT")
    ax2.set_xlabel("ENTROPY_DIFF")
    ax2.set_ylabel("Solve ratio")
    ax2.set_ylim(0, 1.05)
    ax2.legend(title="SIMILAR_LIMIT")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(plot_file)
    print(f"Plot saved to {plot_file}")


def parse_range_arg(arg: str) -> List[float]:
    parts = [p.strip() for p in arg.split(",") if p.strip()]
    return [float(p) for p in parts]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-games", type=int, default=20)
    parser.add_argument("--similar-limits", type=str, default="2,3,4,5")
    parser.add_argument("--entropy-diffs", type=str, default="0.00,0.05,0.10,0.15,0.20")
    parser.add_argument("--csv-file", type=str, default="threshold_experiment_results.csv")
    parser.add_argument("--plot-file", type=str, default="threshold_experiment_plot.png")
    args = parser.parse_args()

    words_path = Path(__file__).parent / "utils" / "words.txt"
    db = WordleDB(words_path)
    words = db.get_words()

    similar_limits = [int(x) for x in args.similar_limits.split(",")]
    entropy_diffs = parse_range_arg(args.entropy_diffs)
    experiments = list(product(similar_limits, entropy_diffs))

    results = run_experiment(words, experiments, args.num_games)
    save_results_csv(results, args.csv_file)
    plot_results(results, args.plot_file)


if __name__ == "__main__":
    main()
