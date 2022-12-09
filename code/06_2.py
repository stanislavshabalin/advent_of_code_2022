import os


def parse_sequence(sequence):
    WINDOW_SIZE = 14
    start = 0
    while len(set(sequence[start : start + WINDOW_SIZE])) < WINDOW_SIZE:
        start += 1

    return start + WINDOW_SIZE


def test():
    assert parse_sequence("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert parse_sequence("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert parse_sequence("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert parse_sequence("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert parse_sequence("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26


def main(input_file):
    test()

    sequence = input_file.read()
    print(parse_sequence(sequence))


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "06.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
