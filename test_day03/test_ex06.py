import string

from pathlib import Path
from typing import Iterable

from more_itertools import grouper


def get_priorities_sum(ruckpacks: Iterable[str]) -> int:
    return sum(
        get_item_priority(get_shared_item(three_ruckpacks))
        for three_ruckpacks in grouper(ruckpacks, 3)
    )


def get_shared_item(ruckpacks: Iterable[str]) -> str:
    ruckpack_sets = (set(ruckpack) for ruckpack in ruckpacks)
    return set.intersection(*ruckpack_sets).pop()  # only one by definition


def get_item_priority(item: str) -> int:
    return string.ascii_letters.index(item) + 1


def test_get_priorities_sum():
    assert (
        get_priorities_sum(
            [
                "vJrwpWtwJgWrhcsFMMfFFhFp",
                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                "PmmdzqPrVvPwwTWBwg",
                "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                "ttgJtRGJQctTZtZT",
                "CrZsJsPPZsGzwwsLwLmpwMDw",
            ]
        )
        == 70
    )


def test_get_shared_item():
    assert (
        get_shared_item(
            [
                "vJrwpWtwJgWrhcsFMMfFFhFp",
                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                "PmmdzqPrVvPwwTWBwg",
            ]
        )
        == "r"
    )


def test_get_item_priority():
    assert get_item_priority("P") == 42
    assert get_item_priority("t") == 20


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        ruckpacks = [line.rstrip("\n") for line in f]
    print(get_priorities_sum(ruckpacks))
