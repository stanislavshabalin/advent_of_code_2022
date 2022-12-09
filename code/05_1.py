import os
import re
from textwrap import dedent


def parse_stacks(stacks_str):
    stacks = {stack: list() for stack in stacks_str[-1].split()}
    stack_names = list(stacks.keys())
    stack_index = 0

    for line in stacks_str[-2::-1]:
        stack_index = 0
        while stack_index < len(stack_names):
            char = line[stack_index * 4 + 1]
            if char != " ":
                stacks[stack_names[stack_index]].append(char)

            stack_index += 1

    return stacks


def parse_move_line(line):
    regex = re.compile(r"move (\d+) from (.+) to (.+)")
    amount, stack_from, stack_to = regex.search(line).groups()
    return int(amount), stack_from, stack_to


def test():
    stacks_str = [
        "[N] [G]                     [Q]    ",
        "[H] [B]         [B] [R]     [H]    ",
        "[S] [N]     [Q] [M] [T]     [Z]    ",
        "[J] [T]     [R] [V] [H]     [R] [S]",
        "[F] [Q]     [W] [T] [V] [J] [V] [M]",
        "[W] [P] [V] [S] [F] [B] [Q] [J] [H]",
        "[T] [R] [Q] [B] [D] [D] [B] [N] [N]",
        "[D] [H] [L] [N] [N] [M] [D] [D] [B]",
        " 1   2   3   4   5   6   7   8   9 ",
    ]

    stacks = {
        "1": ["D", "T", "W", "F", "J", "S", "H", "N"],
        "2": ["H", "R", "P", "Q", "T", "N", "B", "G"],
        "3": ["L", "Q", "V"],
        "4": ["N", "B", "S", "W", "R", "Q"],
        "5": ["N", "D", "F", "T", "V", "M", "B"],
        "6": ["M", "D", "B", "V", "H", "T", "R"],
        "7": ["D", "B", "Q", "J"],
        "8": ["D", "N", "J", "V", "R", "Z", "H", "Q"],
        "9": ["B", "N", "H", "M", "S"],
    }

    assert parse_stacks(stacks_str) == stacks

    assert parse_move_line("move 16 from 6 to 4") == (16, "6", "4")
    assert parse_move_line("move 1 from 7 to 6") == (1, "7", "6")


def main(input_file):
    test()

    stacks_str = []
    stacks = None

    for line in input_file:
        line = line.strip("\n")
        if stacks is None:
            if line:
                stacks_str.append(line)
            else:
                stacks = parse_stacks(stacks_str)

            continue

        amount, stack_from, stack_to = parse_move_line(line.strip())

        stacks[stack_to].extend(stacks[stack_from][-1 : -(amount + 1) : -1])
        stacks[stack_from] = stacks[stack_from][0:-amount]

    print("".join(stack[-1] for stack in stacks.values()))


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "05.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
