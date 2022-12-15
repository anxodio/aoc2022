from pathlib import Path
from typing import Tuple


def is_one_range_fully_contained(sections1: range, sections2: range) -> bool:
    set1, set2 = (set(section) for section in (sections1, sections2))
    return set1.issubset(set2) or set1.issuperset(set2)


def parse_line(line: str) -> Tuple[range, range]:
    #  mypy cries (with reason) about you can't assure that this will be a 2 items tuple
    #  return tuple(
    #     range(int(start), int(end) + 1)
    #     for start, end in (elf.split("-") for elf in line.split(","))
    # )
    raw1, raw2 = line.split(",")
    raw_start1, raw_end1 = raw1.split("-")
    raw_start2, raw_end2 = raw2.split("-")
    return range(int(raw_start1), int(raw_end1) + 1), range(
        int(raw_start2), int(raw_end2) + 1
    )


def test_is_one_range_fully_contained():
    assert is_one_range_fully_contained(range(2, 5), range(6, 9)) is False
    assert is_one_range_fully_contained(range(2, 9), range(3, 8)) is True


def test_parse_line():
    assert parse_line("2-4,6-8") == (range(2, 5), range(6, 9))
    assert parse_line("2-8,3-7") == (range(2, 9), range(3, 8))


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        section_pairs = [parse_line(line.rstrip("\n")) for line in f]
    print(
        sum(
            1
            for section_pair in section_pairs
            if is_one_range_fully_contained(*section_pair)
        )
    )
