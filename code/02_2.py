import os
from enum import Enum, auto


class Outcome(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


def calc_score(a, outcome):
    a, outcome = map(str.lower, (a, outcome))
    outcomes = {
        "x": Outcome.LOSE,
        "y": Outcome.DRAW,
        "z": Outcome.WIN,
    }
    outcome = outcomes[outcome]

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

    game = next(
        filter(
            lambda dict_item: (dict_item[0][0] == a and outcome == dict_item[1]),
            rules.items(),
        )
    )

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

    return outcome_score[outcome] + choice_score[game[0][1]]


def main(input_file):
    score = 0
    for line in input_file:
        if not line.strip():
            continue

        elf, outcome = map(str.strip, line.strip().split())
        score += calc_score(elf, outcome)

    print(score)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "02.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
