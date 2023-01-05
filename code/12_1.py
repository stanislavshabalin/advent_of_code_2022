import os

from collections import defaultdict, namedtuple


Square = namedtuple("Square", ["x", "y"])


class Node:
    def __init__(self):
        self.edges = []

    def __repr__(self):
        return str(len(self.edges))


class CoordsValidator:
    def __init__(self, max_x, max_y):
        self._max_x = max_x
        self._max_y = max_y

    def validate_coords(self, x, y):
        if x < 0 or y < 0:
            return False

        if x > self._max_x or y > self._max_y:
            return False

        return True


def main(input_file):
    grid = []
    for line in input_file:
        grid.append(list(line.strip()))

    graph = {}
    begin_node, end_node = None, None

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            square = Square(x=x, y=y)
            graph[square] = Node()

            if grid[x][y] == "S":
                grid[x][y] = "a"
                begin_node = graph[square]

            if grid[x][y] == "E":
                grid[x][y] = "z"
                end_node = graph[square]

    validator = CoordsValidator(len(grid) - 1, len(grid[0]) - 1)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            square = Square(x=x, y=y)
            for delta_x, delta_y in ((-1, 0), (0, 1), (1, 0), (0, -1)):
                next_square = Square(x=x + delta_x, y=y + delta_y)
                if not validator.validate_coords(next_square.x, next_square.y):
                    continue

                next_letter = grid[next_square.x][next_square.y]
                this_letter = grid[square.x][square.y]
                if ord(next_letter) - ord(this_letter) <= 1:
                    graph[square].edges.append(graph[next_square])


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "12.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
