import os
import operator
from functools import reduce


def _calc_priority(char):
    lower_shift = ord("a") - 1
    upper_shift = (ord("A") - 1) - 26
    if char.islower():
        return ord(char) - lower_shift

    return ord(char) - upper_shift


def test():
    assert _calc_priority("a") == 1
    assert _calc_priority("z") == 26
    assert _calc_priority("A") == 27
    assert _calc_priority("Z") == 52


def main(input_file):
    test()

    GROUP_SIZE = 3
    priority = 0
    group = []

    for line in input_file:
        rucksack = line.strip()

        group.append(set(rucksack))
        if len(group) >= GROUP_SIZE:
            item = reduce(operator.and_, group)
            priority += _calc_priority(next(iter(item)))

            group = []

    print(priority)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "03_1.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
