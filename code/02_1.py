import os
from enum import Enum, auto


class Outcome(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


def calc_score(a, b):
    a, b = map(str.lower, (a, b))
    rules = {
        ("a", "x"): Outcome.DRAW,
        ("a", "y"): Outcome.WIN,
        ("a", "z"): Outcome.LOSE,
        ("b", "x"): Outcome.LOSE,
        ("b", "y"): Outcome.DRAW,
        ("b", "z"): Outcome.WIN,
        ("c", "x"): Outcome.WIN,
        ("c", "y"): Outcome.LOSE,
        ("c", "z"): Outcome.DRAW,
    }

    outcome_score = {
        Outcome.WIN: 6,
        Outcome.DRAW: 3,
        Outcome.LOSE: 0,
    }

    choice_score = {
        "x": 1,
        "y": 2,
        "z": 3,
    }

    return outcome_score[rules[(a, b)]] + choice_score[b]


def main(input_file):
    score = 0
    for line in input_file:
        if not line.strip():
            continue

        elf, me = map(str.strip, line.strip().split())
        score += calc_score(elf, me)

    print(score)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "02.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
