from pathlib import Path
from typing import Iterable


TreeGrid = list[list[int]]


def parse_tree_grid(lines: Iterable[str]) -> TreeGrid:
    return [[int(num) for num in line] for line in lines]


def count_visible_trees(grid: TreeGrid) -> int:
    return sum(
        1
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if is_tree_visible(grid, x, y)
    )


def is_tree_visible(grid: TreeGrid, x: int, y: int) -> bool:
    heigth = grid[x][y]
    return (
        heigth > max(grid[x][0:y] or [-1])
        or heigth > max(grid[x][y + 1 :] or [-1])
        or heigth > max([grid[i][y] for i in range(x + 1, len(grid))] or [-1])
        or heigth > max([grid[i][y] for i in range(x)] or [-1])
    )


def test_parse_tree_grid():
    assert parse_tree_grid(["30373", "25512", "65332", "33549", "35390"]) == [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]


def test_is_tree_visible():
    grid = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    assert is_tree_visible(grid, 0, 0) is True
    assert is_tree_visible(grid, 1, 4) is True
    assert is_tree_visible(grid, 4, 2) is True
    assert is_tree_visible(grid, 0, 2) is True
    assert is_tree_visible(grid, 1, 1) is True
    assert is_tree_visible(grid, 1, 2) is True
    assert is_tree_visible(grid, 3, 3) is False
    assert is_tree_visible(grid, 3, 2) is True
    assert is_tree_visible(grid, 0, 1) is True


def test_count_visible_trees():
    assert (
        count_visible_trees(
            [
                [3, 0, 3, 7, 3],
                [2, 5, 5, 1, 2],
                [6, 5, 3, 3, 2],
                [3, 3, 5, 4, 9],
                [3, 5, 3, 9, 0],
            ]
        )
        == 21
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
    grid = parse_tree_grid(lines)
    print(count_visible_trees(grid))
