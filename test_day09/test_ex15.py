from pathlib import Path
from dataclasses import dataclass, field


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


@dataclass
class RopeSimulator:
    head: Position = Position(0, 0)
    tail: Position = Position(0, 0)
    _tail_visited_tiles: set[Position] = field(default_factory=set)

    def move(self, direction: Direction, steps: int) -> None:
        for _ in range(steps):
            self.head = self.head.get_next_position(direction)
            self._move_tail_if_needed()
            self._tail_visited_tiles.add(self.tail)

    def count_tail_visited_tiles(self) -> int:
        return len(self._tail_visited_tiles)

    def _move_tail_if_needed(self) -> None:
        x_diff = self.head.x - self.tail.x
        y_diff = self.head.y - self.tail.y

        if abs(x_diff) > 1:
            delta = -x_diff // abs(x_diff)
            y_position = self.tail.y if y_diff == 0 else self.head.y
            self.tail = Position(self.head.x + delta, y_position)

        if abs(y_diff) > 1:
            delta = -y_diff // abs(y_diff)
            x_position = self.tail.x if x_diff == 0 else self.head.x
            self.tail = Position(x_position, self.head.y + delta)


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


def test_simulation_horizontal_moving():
    simulator = RopeSimulator()
    simulator.move(RIGHT, 5)
    assert simulator.head == Position(5, 0)
    assert simulator.tail == Position(4, 0)
    simulator.move(LEFT, 3)
    assert simulator.head == Position(2, 0)
    assert simulator.tail == Position(3, 0)


def test_simulation_vertical_moving():
    simulator = RopeSimulator()
    simulator.move(DOWN, 5)
    assert simulator.head == Position(0, -5)
    assert simulator.tail == Position(0, -4)
    simulator.move(UP, 3)
    assert simulator.head == Position(0, -2)
    assert simulator.tail == Position(0, -3)


def test_simulation_diagonal_moving():
    simulator = RopeSimulator()
    simulator.move(RIGHT, 2)
    simulator.move(UP, 1)
    assert simulator.head == Position(2, 1)
    assert simulator.tail == Position(1, 0)
    simulator.move(UP, 1)
    assert simulator.head == Position(2, 2)
    assert simulator.tail == Position(2, 1)
    simulator.move(LEFT, 2)
    assert simulator.head == Position(0, 2)
    assert simulator.tail == Position(1, 2)


def test_simulation_count_tail_visited_tiles():
    simulator = RopeSimulator()
    simulator.move(RIGHT, 4)
    simulator.move(UP, 4)
    simulator.move(LEFT, 3)
    simulator.move(DOWN, 1)
    simulator.move(RIGHT, 4)
    simulator.move(DOWN, 1)
    simulator.move(LEFT, 5)
    simulator.move(RIGHT, 2)
    assert simulator.count_tail_visited_tiles() == 13


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
