import os


def parse_sequence(sequence):
    WINDOW_SIZE = 4
    start = 0
    while len(set(sequence[start : start + WINDOW_SIZE])) < WINDOW_SIZE:
        start += 1

    return start + WINDOW_SIZE


def test():
    assert parse_sequence("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert parse_sequence("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert parse_sequence("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert parse_sequence("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert parse_sequence("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11


def main(input_file):
    test()

    sequence = input_file.read()
    print(parse_sequence(sequence))


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "06.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
