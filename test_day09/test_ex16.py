from pathlib import Path
from dataclasses import dataclass
from itertools import pairwise


@dataclass(frozen=True)
class Direction:
    delta_x: int
    delta_y: int


RIGHT = Direction(1, 0)
LEFT = Direction(-1, 0)
UP = Direction(0, 1)
DOWN = Direction(0, -1)


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def get_next_position(self, direction: Direction) -> "Position":
        return Position(self.x + direction.delta_x, self.y + direction.delta_y)


class RopeSimulator:
    def __init__(self, rope_length: int = 10) -> None:
        self.rope: list[Position] = [Position(0, 0)] * rope_length
        self._tail_visited_tiles: set[Position] = set()

    @property
    def head(self) -> Position:
        return self.rope[0]

    @property
    def tail(self) -> Position:
        return self.rope[-1]

    def move(self, direction: Direction, steps: int) -> None:
        for _ in range(steps):
            self.rope[0] = self.head.get_next_position(direction)
            for i_actual, i_next in pairwise(range(len(self.rope))):
                self._move_next_if_needed(i_actual, i_next)
            self._tail_visited_tiles.add(self.tail)

    def count_tail_visited_tiles(self) -> int:
        return len(self._tail_visited_tiles)

    def _move_next_if_needed(self, i_actual: int, i_next: int) -> None:
        x_diff = self.rope[i_actual].x - self.rope[i_next].x
        y_diff = self.rope[i_actual].y - self.rope[i_next].y

        if max(abs(x_diff), abs(y_diff)) > 1:
            self.rope[i_next] = Position(
                self.rope[i_next].x + (x_diff // abs(x_diff) if x_diff else 0),
                self.rope[i_next].y + (y_diff // abs(y_diff) if y_diff else 0),
            )


def parse_line(raw_line: str) -> tuple[Direction, int]:
    _mapper = {"R": RIGHT, "L": LEFT, "U": UP, "D": DOWN}
    raw_dir, raw_count = raw_line.split()
    return _mapper[raw_dir], int(raw_count)


def test_simuator_creation():
    simulator = RopeSimulator()
    assert simulator.head == Position(0, 0)
    assert simulator.tail == Position(0, 0)


def test_direction_get_next_position():
    assert Position(2, 6).get_next_position(RIGHT) == Position(3, 6)
    assert Position(2, 6).get_next_position(LEFT) == Position(1, 6)


def test_simulation_moving():
    simulator = RopeSimulator()
    simulator.move(RIGHT, 5)
    simulator.move(UP, 8)
    simulator.move(LEFT, 8)
    assert simulator.head == Position(-3, 8)
    assert simulator.tail == Position(1, 3)
    simulator.move(DOWN, 3)
    simulator.move(RIGHT, 17)
    assert simulator.head == Position(14, 5)
    assert simulator.tail == Position(5, 5)


def test_simulation_moving_special_diagonal():
    simulator = RopeSimulator(3)
    simulator.move(LEFT, 2)
    simulator.move(DOWN, 2)
    assert simulator.head == Position(-2, -2)
    assert simulator.tail == Position(-1, -1)


def test_simulation_count_tail_visited_tiles():
    simulator = RopeSimulator()
    simulator.move(RIGHT, 5)
    simulator.move(UP, 8)
    simulator.move(LEFT, 8)
    simulator.move(DOWN, 3)
    simulator.move(RIGHT, 17)
    simulator.move(DOWN, 10)
    simulator.move(LEFT, 25)
    simulator.move(UP, 20)
    assert simulator.count_tail_visited_tiles() == 36


def test_parse_line():
    assert parse_line("R 4") == (RIGHT, 4)
    assert parse_line("U 4") == (UP, 4)
    assert parse_line("L 3") == (LEFT, 3)
    assert parse_line("D 1") == (DOWN, 1)


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]

    simulator = RopeSimulator()
    for line in lines:
        simulator.move(*parse_line(line))
    print(simulator.count_tail_visited_tiles())
