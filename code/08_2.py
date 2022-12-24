import os
import operator

from functools import reduce


class GridCell:
    def __init__(self, i, j, max_i, max_j):
        self.cell_i, self.cell_j = i, j
        self.max_i, self.max_j = max_i, max_j

    def _validate_coords(self, i, j):
        if i < 0 or j < 0:
            return False

        if i > self.max_i or j > self.max_j:
            return False

        return True

    def go_up(self):
        i, j = self.cell_i, self.cell_j
        while self._validate_coords(i - 1, j):
            i -= 1
            yield i, j

    def go_right(self):
        i, j = self.cell_i, self.cell_j
        while self._validate_coords(i, j + 1):
            j += 1
            yield i, j

    def go_down(self):
        i, j = self.cell_i, self.cell_j
        while self._validate_coords(i + 1, j):
            i += 1
            yield i, j

    def go_left(self):
        i, j = self.cell_i, self.cell_j
        while self._validate_coords(i, j - 1):
            j -= 1
            yield i, j


def score_tree(grid, i, j):
    tree = GridCell(i, j, len(grid) - 1, len(grid[0]) - 1)

    generators = tree.go_up(), tree.go_right(), tree.go_down(), tree.go_left()

    scores = []

    for generator in generators:
        score = 0
        current_height = None
        for gen_i, gen_j in generator:
            if current_height is None:
                current_height = grid[gen_i][gen_j]
                score += 1
            elif grid[gen_i][gen_j] >= current_height:
                current_height = grid[gen_i][gen_j]
                score += 1

        scores.append(score)

    print(f"{grid[i][j]}: {scores}")
    return reduce(operator.mul, scores)


def parse_grid(grid):
    max_i = len(grid) - 1
    max_j = len(grid[0]) - 1

    max_score = -1
    for i in range(1, max_i):
        for j in range(1, max_j):
            max_score = max(max_score, score_tree(grid, i, j))

    return max_score


def _process_line(trees: str) -> list:
    processed_line = []

    for height in trees:
        processed_line.append(int(height))

    return processed_line


def main(input_file):
    grid = []

    for line in input_file:
        line = line.strip()
        if line:
            next_line = _process_line(line)

            grid.append(next_line)

    max_tree_score = parse_grid(grid)

    print(max_tree_score)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "08.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
