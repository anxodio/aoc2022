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
    def __init__(self, instructions: list[Instruction]) -> None:
        self._cycle: int = 0
        self._register: int = 1
        self._instuctions: list[Instruction] = instructions

    def __iter__(self) -> Generator[int, None, None]:
        for instruction in self._instuctions:
            for value in instruction.execute():
                signal_strength = (self.cycle + 1) * self.register
                self._cycle += 1
                self._register += value if value else 0
                yield signal_strength

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


def test_signal_strength():
    cpu = InstructionProcessor(
        [
            AddxInstruction(15),
            AddxInstruction(-11),
            AddxInstruction(6),
            AddxInstruction(-3),
            AddxInstruction(5),
            AddxInstruction(-1),
            AddxInstruction(-8),
            AddxInstruction(13),
            AddxInstruction(4),
            NoopInstruction(),
            AddxInstruction(-1),
            AddxInstruction(5),
            AddxInstruction(-1),
            AddxInstruction(5),
            AddxInstruction(-1),
            AddxInstruction(5),
            AddxInstruction(-1),
            AddxInstruction(5),
            AddxInstruction(-1),
            AddxInstruction(-35),
            AddxInstruction(1),
            AddxInstruction(24),
            AddxInstruction(-19),
        ]
    )
    for i, signal_strenght in enumerate(cpu):
        if i + 1 == 20:
            assert signal_strenght == 420


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        instructions = [parse_line(line.rstrip("\n")) for line in f]

    cpu = InstructionProcessor(instructions)
    total_signal_strenght = 0
    for i, signal_strenght in enumerate(cpu):
        if i + 1 in (20, 60, 100, 140, 180, 220):
            total_signal_strenght += signal_strenght
    print(total_signal_strenght)
