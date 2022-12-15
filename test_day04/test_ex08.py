from pathlib import Path
from typing import Tuple


def are_ranges_overlapping(sections1: range, sections2: range) -> bool:
    set1, set2 = (set(section) for section in (sections1, sections2))
    return bool(set1.intersection(set2))


def parse_line(line: str) -> Tuple[range, range]:
    raw1, raw2 = line.split(",")
    raw_start1, raw_end1 = raw1.split("-")
    raw_start2, raw_end2 = raw2.split("-")
    return range(int(raw_start1), int(raw_end1) + 1), range(
        int(raw_start2), int(raw_end2) + 1
    )


def test_are_ranges_overlapping():
    assert are_ranges_overlapping(range(2, 5), range(6, 9)) is False
    assert are_ranges_overlapping(range(2, 9), range(3, 8)) is True
    assert are_ranges_overlapping(range(5, 8), range(7, 10)) is True


def test_parse_line():
    assert parse_line("2-4,6-8") == (range(2, 5), range(6, 9))
    assert parse_line("2-8,3-7") == (range(2, 9), range(3, 8))


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        section_pairs = [parse_line(line.rstrip("\n")) for line in f]
    print(
        sum(
            1 for section_pair in section_pairs if are_ranges_overlapping(*section_pair)
        )
    )
