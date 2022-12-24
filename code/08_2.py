import os


def main(input_file):
    for line in input_file:
        pass

    print(42)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "08.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
