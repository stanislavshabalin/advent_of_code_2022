import os


def _calc_priority(char):
    lower_shift = ord("a") - 1
    upper_shift = (ord("A") - 1) - 26
    if char.islower():
        return ord(char) - lower_shift

    return ord(char) - upper_shift


def main(input_file):
    priority = 0
    assert _calc_priority("a") == 1
    assert _calc_priority("z") == 26
    assert _calc_priority("A") == 27
    assert _calc_priority("Z") == 52

    for line in input_file:
        rucksack = line.strip()
        middle = len(rucksack) // 2
        item_set = set(rucksack[:middle]) & set(rucksack[middle:])
        item = next(iter(item_set))
        priority += _calc_priority(item)

    print(priority)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "03.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
