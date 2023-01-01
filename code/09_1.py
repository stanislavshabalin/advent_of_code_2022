import os


class Rope:
    def __init__(self):
        self.head_x, self.head_y = 0, 0
        self.tail_x, self.tail_y = 0, 0

    def _move_head(self, delta_x, delta_y):
        self.head_x += delta_x
        self.head_y += delta_y

    def _move_tail(self):
        abs_x = abs(self.tail_x - self.head_x)
        abs_y = abs(self.tail_y - self.head_y)
        if self.tail_x == self.head_x and abs_y == 2:
            self.tail_y = (self.tail_y + self.head_y) // 2
        elif self.tail_y == self.head_y and abs_x == 2:
            self.tail_x = (self.tail_x + self.head_x) // 2
        elif abs_x == 1 and abs_y == 2:
            self.tail_x = self.head_x
            self.tail_y = (self.tail_y + self.head_y) // 2
        elif abs_x == 2 and abs_y == 1:
            self.tail_y = self.head_y
            self.tail_x = (self.tail_x + self.head_x) // 2

    def move_head(self, delta_x, delta_y):
        old_head = self.head_x, self.head_y
        old_tail = self.tail_x, self.tail_y

        self._move_head(delta_x, delta_y)
        self._move_tail()

        new_head = self.head_x, self.head_y
        new_tail = self.tail_x, self.tail_y

        return self.tail_x, self.tail_y


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
    rope = Rope()
    visited = set()

    for line in input_file:
        moves = parse_input_line(line)
        for delta_x, delta_y in moves:
            visited.add(rope.move_head(delta_x, delta_y))

    print(len(visited))


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "09.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
