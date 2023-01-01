import os
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


class Rope:
    def __init__(self, knots_amount):
        self.head = Point(x=0, y=0)
        self.knots = {}
        self.tail_index = knots_amount

        for knot in range(1, knots_amount + 1):
            self.knots[knot] = Point(x=0, y=0)

    def print_field(self, size=10):
        field = []
        for x in range(0, size):
            field.append(list(".") * size)

        for knot in range(self.tail_index, 0, -1):
            field[self.knots[knot].x][self.knots[knot].y] = str(knot)

        field[self.head.x][self.head.y] = "H"

        for x in range(0, len(field)):
            for y in range(0, len(field[0])):
                print(field[x][y], end="")
            print("\n")
        print("\n")

    def _move_head(self, delta_x, delta_y):
        self.head = Point(x=self.head.x + delta_x, y=self.head.y + delta_y)

    def _move_knots(self):
        self._move_knot(1, self.head)
        for knot_index in range(2, self.tail_index + 1):
            self._move_knot(knot_index, self.knots[knot_index - 1])

    def _move_knot(self, knot_index, prev_knot):
        knot = self.knots[knot_index]
        abs_x = abs(prev_knot.x - knot.x)
        abs_y = abs(prev_knot.y - knot.y)

        avg_x = (knot.x + prev_knot.x) // 2
        avg_y = (knot.y + prev_knot.y) // 2

        if knot.x == prev_knot.x and abs_y == 2:
            self.knots[knot_index] = Point(x=knot.x, y=avg_y)
        elif knot.y == prev_knot.y and abs_x == 2:
            self.knots[knot_index] = Point(x=avg_x, y=knot.y)
        elif abs_x == 1 and abs_y == 2:
            self.knots[knot_index] = Point(x=prev_knot.x, y=avg_y)
        elif abs_x == 2 and abs_y == 1:
            self.knots[knot_index] = Point(x=avg_x, y=prev_knot.y)
        elif abs_x == 2 and abs_y == 2:
            self.knots[knot_index] = Point(x=avg_x, y=avg_y)

    def move_head(self, delta_x, delta_y):
        self._move_head(delta_x, delta_y)
        self._move_knots()

        return self.knots[self.tail_index]


def parse_input_line(line):
    deltas = {
        "U": (0, 1),
        "R": (1, 0),
        "D": (0, -1),
        "L": (-1, 0),
    }

    direction, count = line.split(" ")
    return [deltas[direction]] * int(count)


def main(input_file):
    rope = Rope(knots_amount=9)
    visited = set()

    for line in input_file:
        moves = parse_input_line(line)
        for delta_x, delta_y in moves:
            new_tail = rope.move_head(delta_x, delta_y)
            visited.add(new_tail)

    print(len(visited))


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "09.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
