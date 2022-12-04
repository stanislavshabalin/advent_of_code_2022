import os


def main(input_file):
    POOL_SIZE = 3
    pool = []

    current = 0
    for line in input_file:
        calories = None
        line = line.strip()
        if line:
            calories = int(line, 10)
            current += calories
        else:
            pool.append(current)
            pool = list(sorted(pool, reverse=True)[:POOL_SIZE])
            current = 0

    if current:
        pool.append(current)
        pool = list(sorted(pool, reverse=True)[:POOL_SIZE])

    print(sum(pool))


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "01.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
