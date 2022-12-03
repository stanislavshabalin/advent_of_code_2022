import os


def main(input_file):
    max_calories = 0
    current = 0
    for line in input_file:
        calories = None
        line = line.strip()
        if line:
            calories = int(line, 10)
            current += calories
        else:
            max_calories = max(max_calories, current)
            current = 0

    if current:
        max_calories = max(max_calories, current)

    print(max_calories)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "01_1.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
