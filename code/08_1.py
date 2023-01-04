import os
import pytest
from typing import List
from textwrap import dedent


class LineOfSight:
    def __init__(self):
        self.current_height = None

    def is_visible(self, height: int) -> bool:
        if self.current_height is None:
            self.current_height = height
            return True

        if self.current_height < height:
            self.current_height = height
            return True

        return False


def _process_line(trees: str) -> list:
    processed_line = []

    for height in trees:
        processed_line.append([int(height), None])

    return processed_line


def parse_grid(grid: List[List[int]]) -> int:
    total_visible = 0

    horizontal_ranges = (
        # horizontal left-to-right
        (range(0, len(grid)), range(0, len(grid[0]))),
        # horizontal right-to-left
        (range(0, len(grid)), range(len(grid[0]) - 1, -1, -1)),
    )

    for i_range, j_range in horizontal_ranges:
        for i in i_range:
            los = LineOfSight()
            for j in j_range:
                current_tree = grid[i][j]
                is_visible = los.is_visible(current_tree[0])
                if current_tree[1] is None:
                    current_tree[1] = is_visible
                    total_visible += int(is_visible)

                if is_visible and not current_tree[1]:
                    grid[i][j][1] = True
                    total_visible += 1

    vertical_ranges = (
        # vertical top-to-bottom
        (range(0, len(grid)), range(0, len(grid[0]))),
        # vertical bottom-to-top
        (range(len(grid) - 1, -1, -1), range(0, len(grid[0]))),
    )

    for i_range, j_range in vertical_ranges:
        for j in j_range:
            los = LineOfSight()
            for i in i_range:
                current_tree = grid[i][j]
                is_visible = los.is_visible(current_tree[0])
                if is_visible and not current_tree[1]:
                    grid[i][j][1] = True
                    total_visible += 1

    return total_visible


def main(input_file):
    grid = []

    for line in input_file:
        line = line.strip()
        if line:
            next_line = _process_line(line)

            grid.append(next_line)

    total_visible = parse_grid(grid)

    print(total_visible)


@pytest.mark.parametrize(
    "tree_vector, expected_sights",
    (
        (
            "121",
            (True, True, False),
        ),
        (
            "123",
            (True, True, True),
        ),
        (
            "231",
            (True, True, False),
        ),
        (
            "321",
            (True, False, False),
        ),
        (
            "111",
            (True, False, False),
        ),
        (
            "515627",
            (True, False, False, True, False, True),
        ),
        (
            "5123665271",
            (True, False, False, False, True, False, False, False, True, False),
        ),
        (
            "3037053",
            (True, False, False, True, False, False, False),
        ),
        (
            "00042",
            (True, False, False, True, False),
        ),
    ),
)
def test_line_of_sight(tree_vector, expected_sights):
    los = LineOfSight()
    result = tuple(los.is_visible(int(tree_height)) for tree_height in tree_vector)

    assert result == expected_sights


@pytest.mark.parametrize(
    "grid, expected_sights",
    (
        (
            """
            121
            131
            121
            """,
            """
            111
            111
            111
            """,
        ),
        (
            """
            323
            111
            323
            """,
            """
            111
            101
            111
            """,
        ),
        (
            """
            14641
            12311
            32222
            43334
            12241
            """,
            """
            11111
            11101
            10001
            11101
            11111
            """,
        ),
        (
            """
            55555
            51115
            51115
            51115
            55555
            """,
            """
            11111
            10001
            10001
            10001
            11111
            """,
        ),
        (
            """
            55555
            51115
            51715
            51115
            55555
            """,
            """
            11111
            10001
            10101
            10001
            11111
            """,
        ),
        (
            """
            4444
            1111
            2222
            1111
            """,
            """
            1111
            1001
            1111
            1111
            """,
        ),
        (
            """
            9
            """,
            """
            1
            """,
        ),
        (
            """
            55
            55
            """,
            """
            11
            11
            """,
        ),
        (
            """
            9876
            8765
            7654
            6543
            """,
            """
            1111
            1111
            1111
            1111
            """,
        ),
        (
            """
            552255
            545545
            611116
            611116
            545545
            551144
            """,
            """
            111111
            101101
            100001
            100001
            101101
            111111
            """,
        ),
    ),
)
def test_parse_grid(grid, expected_sights):
    def _str_to_grid(trees):
        trees = dedent(trees).split("\n")
        grid = []
        for line in trees:
            line = line.strip()
            if line:
                grid.append(_process_line(line))

        return grid

    def _grid_to_str(grid):
        result = ""
        for line in grid:
            for tree in line:
                if tree[1] is None:
                    result += "N"
                else:
                    result += str(int(tree[1]))
            result += "\n"

        return result.strip()

    grid = _str_to_grid(dedent(grid))

    visible = parse_grid(grid)

    assert _grid_to_str(grid) == dedent(expected_sights).strip()
    assert visible == expected_sights.count("1")


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "08.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
