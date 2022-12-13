from pathlib import Path
from typing import List, Generator
from itertools import takewhile


def get_most_calories(chunks_of_calories: List[List[int]]) -> int:
    added_calories = [sum(group) for group in chunks_of_calories]
    return max(added_calories)


def generate_chunks_of_lines(raw_lines: List[str]) -> Generator[List[str], None, None]:
    raw_lines_iterator = iter(raw_lines)
    while lines := list(takewhile(lambda line: line != "", raw_lines_iterator)):
        yield lines


def test_get_most_calories():
    assert (
        get_most_calories(
            [
                [
                    1000,
                    2000,
                    3000,
                ],
                [
                    4000,
                ],
                [
                    5000,
                    6000,
                ],
                [
                    7000,
                    8000,
                    9000,
                ],
                [
                    10000,
                ],
            ]
        )
        == 24000
    )


def test_generate_chunks_of_lines() -> None:
    assert list(
        generate_chunks_of_lines(["a", "b", "", "c", "d", "", "e", "f", "g"])
    ) == [["a", "b"], ["c", "d"], ["e", "f", "g"]]


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        raw_lines = [line.rstrip("\n") for line in f]
    lines = [int(line) if line else "" for line in raw_lines]
    chunks_of_calories = generate_chunks_of_lines(lines)
    print(get_most_calories(chunks_of_calories))
