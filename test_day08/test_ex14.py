from pathlib import Path
from typing import Iterable


TreeGrid = list[list[int]]


def parse_tree_grid(lines: Iterable[str]) -> TreeGrid:
    return [[int(num) for num in line] for line in lines]


def get_max_scenic_score(grid: TreeGrid) -> int:
    return max(
        get_scenic_score(grid, x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
    )


def get_scenic_score(grid: TreeGrid, x: int, y: int) -> int:
    heigth = grid[x][y]

    right = grid[x][y + 1 :]
    left = grid[x][0:y][::-1]
    down = [grid[i][y] for i in range(x + 1, len(grid))]
    up = [grid[i][y] for i in range(x)][::-1]

    return (
        _get_direction_scenic_score(heigth, right)
        * _get_direction_scenic_score(heigth, left)
        * _get_direction_scenic_score(heigth, down)
        * _get_direction_scenic_score(heigth, up)
    )


def _get_direction_scenic_score(height: int, direction: list[int]) -> int:
    score = 0
    for i in direction:
        score += 1
        if i >= height:
            break
    return score


def test_parse_tree_grid():
    assert parse_tree_grid(["30373", "25512", "65332", "33549", "35390"]) == [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]


def test_get_scenic_score():
    grid = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    assert get_scenic_score(grid, 1, 2) == 4


def test_get_max_scenic_score():
    assert (
        get_max_scenic_score(
            [
                [3, 0, 3, 7, 3],
                [2, 5, 5, 1, 2],
                [6, 5, 3, 3, 2],
                [3, 3, 5, 4, 9],
                [3, 5, 3, 9, 0],
            ]
        )
        == 8
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
    grid = parse_tree_grid(lines)
    print(get_max_scenic_score(grid))
