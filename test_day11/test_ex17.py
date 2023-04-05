from pathlib import Path
from typing import List, Generator, Any
from itertools import takewhile
from dataclasses import dataclass


@dataclass(frozen=True)
class ItemMovement:
    monkey_id: int
    worry_level: int


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: str
    divisible_test: int
    true_target: int
    false_target: int
    inspection_count: int = 0

    def inspect_next_item(self) -> ItemMovement:
        if not self.items:
            raise StopIteration
        old_item = self.items.pop(0)
        new_item = self.do_operation(old_item)
        bored_item = new_item // 3
        target = (
            self.true_target
            if (bored_item % self.divisible_test) == 0
            else self.false_target
        )
        self.inspection_count += 1
        return ItemMovement(target, bored_item)

    def do_operation(self, old_item) -> int:
        return eval(self.operation, {"old": old_item})


def build_monkey_from_text(text: list[str]) -> Monkey:
    # assumes less than 10 monkeys
    id_ = int(text[0].split()[1][0])
    items = [int(i) for i in text[1].split(": ")[1].split(", ")]
    operation = text[2].split("= ")[1]
    divisible_test = int(text[3].split("by ")[1])
    true_target = int(text[4][-1])
    false_target = int(text[5][-1])
    return Monkey(id_, items, operation, divisible_test, true_target, false_target)


def generate_chunks_of_lines(raw_lines: List[Any]) -> Generator[List[Any], None, None]:
    raw_lines_iterator = iter(raw_lines)
    while lines := list(takewhile(lambda line: bool(line), raw_lines_iterator)):
        yield lines


def get_monkey_business_level(monkeys: list[Monkey]) -> int:
    for _ in range(20):
        for monkey in monkeys:
            while monkey.items:
                movement = monkey.inspect_next_item()
                monkeys[movement.monkey_id].items.append(movement.worry_level)
    counts = sorted((monkey.inspection_count for monkey in monkeys), reverse=True)
    return counts[0] * counts[1]


def _get_test_monkeys() -> list[Monkey]:
    monkey0 = build_monkey_from_text(
        [
            "Monkey 0:",
            "Starting items: 79, 98",
            "Operation: new = old * 19",
            "Test: divisible by 23",
            "If true: throw to monkey 2",
            "If false: throw to monkey 3",
        ]
    )
    monkey1 = build_monkey_from_text(
        [
            "Monkey 1:",
            "Starting items: 54, 65, 75, 74",
            "Operation: new = old + 6",
            "Test: divisible by 19",
            "If true: throw to monkey 2",
            "If false: throw to monkey 0",
        ]
    )
    monkey2 = build_monkey_from_text(
        [
            "Monkey 2:",
            "Starting items: 79, 60, 97",
            "Operation: new = old * old",
            "Test: divisible by 13",
            "If true: throw to monkey 1",
            "If false: throw to monkey 3",
        ]
    )
    monkey3 = build_monkey_from_text(
        [
            "Monkey 3:",
            "Starting items: 74",
            "Operation: new = old + 3",
            "Test: divisible by 17",
            "If true: throw to monkey 0",
            "If false: throw to monkey 1",
        ]
    )
    return [monkey0, monkey1, monkey2, monkey3]


def test_build_monkey_from_text():
    monkey = _get_test_monkeys()[0]
    assert monkey.id == 0
    assert monkey.items == [79, 98]
    assert monkey.operation == "old * 19"
    assert monkey.divisible_test == 23
    assert monkey.true_target == 2
    assert monkey.false_target == 3


def test_monkey_operation():
    monkey = _get_test_monkeys()[0]

    monkey.operation = "old * 5"
    assert monkey.do_operation(5) == 25

    monkey.operation = "old * old"
    assert monkey.do_operation(3) == 9


def test_item_inspection():
    monkey = _get_test_monkeys()[0]
    assert monkey.items == [79, 98]
    assert monkey.inspect_next_item() == ItemMovement(3, 500)
    assert monkey.items == [98]
    assert monkey.inspection_count == 1


def test_get_monkey_business_level():
    monkeys = _get_test_monkeys()
    assert get_monkey_business_level(monkeys) == 10605


def test_generate_chunks_of_lines() -> None:
    assert list(
        generate_chunks_of_lines(["a", "b", "", "c", "d", "", "e", "f", "g"])
    ) == [["a", "b"], ["c", "d"], ["e", "f", "g"]]


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        raw_lines = [line.rstrip("\n") for line in f]
    chunks_of_calories = generate_chunks_of_lines(raw_lines)
    monkeys = [build_monkey_from_text(chunk) for chunk in chunks_of_calories]
    print(get_monkey_business_level(monkeys))
