import string

from pathlib import Path
from typing import List


def get_priorities_sum(ruckpacks: List[str]) -> int:
    return sum(get_item_priority(get_shared_item(ruckpack)) for ruckpack in ruckpacks)


def get_shared_item(ruckpack: str) -> str:
    first_compartment = set(ruckpack[: len(ruckpack) // 2])
    second_compartment = set(ruckpack[len(ruckpack) // 2 :])
    return first_compartment.intersection(
        second_compartment
    ).pop()  # only one by definition


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
        == 157
    )


def test_get_shared_item():
    assert get_shared_item("vJrwpWtwJgWrhcsFMMfFFhFp") == "p"
    assert get_shared_item("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL") == "L"
    assert get_shared_item("CrZsJsPPZsGzwwsLwLmpwMDw") == "s"


def test_get_item_priority():
    assert get_item_priority("P") == 42
    assert get_item_priority("t") == 20


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        ruckpacks = [line.rstrip("\n") for line in f]
    print(get_priorities_sum(ruckpacks))
