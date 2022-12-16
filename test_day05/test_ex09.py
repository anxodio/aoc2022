import re
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    quantity: int
    origin: int
    destination: int


def get_top_crates_after_instructions(
    stacks: list[list[str]], instructions: list[Instruction]
) -> str:
    for instruction in instructions:
        for _ in range(instruction.quantity):
            stacks[instruction.destination - 1].append(
                stacks[instruction.origin - 1].pop()
            )
    return "".join(stack[-1] for stack in stacks)


def parse_raw_stacks(raw_stacks: list[str]) -> list[list[str]]:
    spacing_number = 4  # util for calculate positions with int divisions
    ordered_raw_stacks = raw_stacks[:-1][::-1]
    stacks: list[list[str]] = [
        [] for _ in range((len(ordered_raw_stacks[0]) + 1) // spacing_number)
    ]
    for raw_stack in ordered_raw_stacks:
        for i in range(len(raw_stack)):
            if raw_stack[i] == "[":
                stacks[i // spacing_number].append(raw_stack[i + 1])
    return stacks


def parse_instruction(raw_instruction: str) -> Instruction:
    raw_numbers = re.findall(r"move (\d+) from (\d+) to (\d+)", raw_instruction)[0]
    return Instruction(int(raw_numbers[0]), int(raw_numbers[1]), int(raw_numbers[2]))


def test_get_top_crates_after_instructions():
    assert (
        get_top_crates_after_instructions(
            [["Z", "N"], ["M", "C", "D"], ["P"]],
            [
                Instruction(1, 2, 1),
                Instruction(3, 1, 3),
                Instruction(2, 2, 1),
                Instruction(1, 1, 2),
            ],
        )
        == "CMZ"
    )


def test_parse_raw_stacks():
    assert parse_raw_stacks(
        [
            "    [D]    ",
            "[N] [C]    ",
            "[Z] [M] [P]",
            " 1   2   3 ",
        ]
    ) == [["Z", "N"], ["M", "C", "D"], ["P"]]


def test_parse_instruction():
    assert parse_instruction("move 1 from 2 to 1") == Instruction(1, 2, 1)
    assert parse_instruction("move 2 from 2 to 1") == Instruction(2, 2, 1)
    assert parse_instruction("move 11 from 7 to 2") == Instruction(11, 7, 2)


if __name__ == "__main__":
    raw_stacks: list[str] = []
    instructions: list[Instruction] = []
    with open((Path(__file__).parent / "input.txt")) as f:
        for line in f:
            clean_line = line.rstrip("\n")
            if clean_line[0:4] == "move":
                instructions.append(parse_instruction(clean_line))
            elif clean_line != "":
                raw_stacks.append(clean_line)

    stacks = parse_raw_stacks(raw_stacks)
    print(get_top_crates_after_instructions(stacks, instructions))
