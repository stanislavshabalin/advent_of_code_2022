import os
import re
import operator

from functools import reduce
from collections import Counter


class Item:
    def __init__(self, worry):
        self.worry = worry

    def __repr__(self):
        return repr(self.worry)

    def __str__(self):
        return repr(self)


class Monkey:
    def __init__(
        self, operation, divisible_by, monkey_if_true, monkey_if_false
    ):
        self._items = []
        self._inspect_operation = operation
        self._divisible_by = divisible_by
        self._monkey_if_true = monkey_if_true
        self._monkey_if_false = monkey_if_false

    def add_item(self, worry):
        self._items.append(Item(worry))

    def inspect(self):
        if not self._items:
            return None

        item = self._items.pop(0)
        item.worry = self._inspect_operation(item.worry)
        if item.worry % self._divisible_by:
            return item.worry, self._monkey_if_false

        return item.worry, self._monkey_if_true

    def __repr__(self):
        return f"Monkey with items {self._items}"


def parse_operation(op_string):
    OPERATORS = {
        "+": operator.add,
        "-": operator.sub,
        # '/': operator.truediv,
        "*": operator.mul,
    }
    op_parts = op_string.split()
    op_operator = OPERATORS[op_parts[1]]

    try:
        op_left = int(op_parts[0])
    except ValueError:
        op_left = None

    try:
        op_right = int(op_parts[2])
    except ValueError:
        op_right = None

    if op_left is None and op_parts[0] != "old":
        raise ValueError(f"Unknown operation: {op_string}")

    if op_right is None and op_parts[2] != "old":
        raise ValueError(f"Unknown operation: {op_string}")

    if op_left is None and op_right is None:
        return lambda old: op_operator(old, old)

    if op_left is None:
        return lambda old: op_operator(old, op_right)

    return lambda old: op_operator(op_left, op_right)


def print_monkeys(monkeys):
    for ind, monkey in monkeys.items():
        print(f"#{ind}: {monkey}")
        # print(monkey._inspect_operation)
        # print(f"Divisible by {monkey._divisible_by}")
        # print(f"If true  - toss to {monkey._monkey_if_true}")
        # print(f"If false - toss to {monkey._monkey_if_false}")
        # print()


def main(input_file):
    current_monkey = None
    current_items = []
    current_operation = None
    current_divisible_by = None
    current_monkey_if_false = None
    current_monkey_if_true = None
    monkeys = {}

    for line in input_file:
        line = line.strip()
        if match := re.match(r"^Monkey (\d+):$", line):
            if current_monkey is not None:
                monkeys[current_monkey] = Monkey(
                    operation=current_operation,
                    divisible_by=current_divisible_by,
                    monkey_if_true=current_monkey_if_true,
                    monkey_if_false=current_monkey_if_false,
                )
                for item in current_items:
                    monkeys[current_monkey].add_item(item)

            current_monkey = int(match.group(1))
        elif match := re.match(r"^Starting items:([0-9,\s]+)$", line):
            current_items = map(int, match.group(1).strip().split(", "))
        elif match := re.match(r"^Operation: new = (.+)$", line):
            current_operation = parse_operation(match.group(1).strip())
        elif match := re.match(r"^Test: divisible by (\d+)$", line):
            current_divisible_by = int(match.group(1))
        elif match := re.match(r"^If true: throw to monkey (\d+)$", line):
            current_monkey_if_true = int(match.group(1))
        elif match := re.match(r"^If false: throw to monkey (\d+)$", line):
            current_monkey_if_false = int(match.group(1))

    monkeys[current_monkey] = Monkey(
        operation=current_operation,
        divisible_by=current_divisible_by,
        monkey_if_true=current_monkey_if_true,
        monkey_if_false=current_monkey_if_false,
    )
    for item in current_items:
        monkeys[current_monkey].add_item(item)

    monkey_inspections = Counter()
    for _ in range(200):
        for monkey in monkeys:
            while result := monkeys[monkey].inspect():
                monkey_inspections[monkey] += 1
                item, toss_to_monkey = result
                monkeys[toss_to_monkey].add_item(item)

    print(monkey_inspections)
    print(
        reduce(
            operator.mul,
            (count for monkey, count in monkey_inspections.most_common(2)),
        )
    )


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "11.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
