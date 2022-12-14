import os


def does_contain(a, b, x, y):
    left = min((a, b), (x, y))
    right = max((a, b), (x, y))

    return right[1] <= left[1] or right[0] == left[0]


def test():
    assert does_contain(1, 1, 2, 4) == False
    assert does_contain(1, 3, 2, 4) == False
    assert does_contain(1, 4, 1, 4) == True
    assert does_contain(1, 4, 1, 1) == True
    assert does_contain(1, 4, 2, 3) == True
    assert does_contain(1, 4, 1, 3) == True


def main(input_file):
    test()

    total = 0

    for line in input_file:
        elf1, elf2 = line.strip().split(",")
        a, b = map(int, elf1.split("-"))
        x, y = map(int, elf2.split("-"))
        if does_contain(a, b, x, y):
            total += 1

    print(total)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "04.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
