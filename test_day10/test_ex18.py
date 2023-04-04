from typing import Any, Generator
from pathlib import Path
from abc import ABC


class Instruction(ABC):
    def __init__(self, argument: int | None = None) -> None:
        self.argument = argument

    def execute(self) -> Generator[int | None, None, None]:
        yield None

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.argument == other.argument
        return False

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.argument})"


class NoopInstruction(Instruction):
    ...


class AddxInstruction(Instruction):
    def execute(self) -> Generator[int | None, None, None]:
        yield None
        yield self.argument


class InstructionProcessor:
    WIDTH = 40

    def __init__(self, instructions: list[Instruction]) -> None:
        self._cycle: int = 0
        self._register: int = 1
        self._instuctions: list[Instruction] = instructions

    def __iter__(self) -> Generator[str, None, None]:
        for instruction in self._instuctions:
            for value in instruction.execute():
                pixel = "."
                if (self.register - 1) <= (self.cycle % self.WIDTH) < self.register + 2:
                    pixel = "#"
                self._cycle += 1
                self._register += value if value else 0
                yield pixel

    def paint(self) -> str:
        printed = ""
        for i, pixel in enumerate(self):
            if i % self.WIDTH == 0:
                printed += "\n"
            printed += pixel
        return printed

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def register(self) -> int:
        return self._register


def parse_line(raw_line: str) -> Instruction:
    if raw_line == "noop":
        return NoopInstruction()
    _, raw_argument = raw_line.split()
    return AddxInstruction(int(raw_argument))


def test_parse_line():
    assert parse_line("noop") == NoopInstruction()
    assert parse_line("addx -3") == AddxInstruction(-3)


def test_empty_processor():
    cpu = InstructionProcessor([])
    flag = True
    for _ in cpu:
        flag = False
    assert flag


def test_simple_noop_processor():
    cpu = InstructionProcessor([NoopInstruction(), NoopInstruction()])
    for _ in cpu:
        ...
    assert cpu.cycle == 2
    assert cpu.register == 1


def test_addx_processor():
    cpu = InstructionProcessor([AddxInstruction(2)])
    for _ in cpu:
        ...
    assert cpu.cycle == 2
    assert cpu.register == 3


def test_combined_processor():
    cpu = InstructionProcessor(
        [NoopInstruction(), AddxInstruction(3), AddxInstruction(-5)]
    )
    for _ in cpu:
        ...
    assert cpu.cycle == 5
    assert cpu.register == -1


def test_iterative_painting():
    cpu = InstructionProcessor(
        [AddxInstruction(15), AddxInstruction(-11), AddxInstruction(6)]
    )
    assert "".join(cpu) == "##..##"


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        instructions = [parse_line(line.rstrip("\n")) for line in f]

    cpu = InstructionProcessor(instructions)
    print(cpu.paint())
