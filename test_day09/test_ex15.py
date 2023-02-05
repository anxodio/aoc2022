from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class Direction:
    delta_x: int
    delta_y: int

    def get_next_position(self, position: Position) -> Position:
        return Position(position.x + self.delta_x, position.y + self.delta_y)


@dataclass
class RopeSimulator:
    head: Position = Position(0, 0)
    tail: Position = Position(0, 0)

    def move(self, direction: Direction, steps: int) -> None:
        for _ in range(steps):
            self.head = direction.get_next_position(self.head)
            self._move_tail_if_needed()

    def _move_tail_if_needed(self) -> None:
        pass


RIGHT = Direction(1, 0)


def test_simuator_creation():
    simulator = RopeSimulator()
    assert simulator.head == Position(0, 0)
    assert simulator.tail == Position(0, 0)


def test_direction_get_next_position():
    assert RIGHT.get_next_position(Position(2, 6)) == Position(3, 6)


def test_simulation_moving():
    simulator = RopeSimulator()
    simulator.move(RIGHT, 3)
    assert simulator.head == Position(3, 0)
    # assert simulator.tail == Position(2, 0)


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
