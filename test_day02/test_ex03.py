from pathlib import Path
from typing import Dict, Tuple, Iterable
from enum import StrEnum, auto


class Hand(StrEnum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


shape_score: Dict[Hand, int] = {
    Hand.ROCK: 1,
    Hand.PAPER: 2,
    Hand.SCISSORS: 3,
}

opponent_to_hand: Dict[str, Hand] = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS,
}

player_to_hand: Dict[str, Hand] = {
    "X": Hand.ROCK,
    "Y": Hand.PAPER,
    "Z": Hand.SCISSORS,
}


def get_total_score(rounds: Iterable[Tuple[Hand, Hand]]):
    return sum(get_round_score(*hands) for hands in rounds)


def get_round_score(opponent_hand: Hand, my_hand: Hand) -> int:
    outcome_score = 0
    if opponent_hand == my_hand:
        outcome_score = 3
    elif opponent_loses(opponent_hand, my_hand):
        outcome_score = 6
    return outcome_score + shape_score[my_hand]


def opponent_loses(opponent_hand: Hand, my_hand: Hand) -> bool:
    return (
        (my_hand == Hand.ROCK and opponent_hand == Hand.SCISSORS)
        or (my_hand == Hand.SCISSORS and opponent_hand == Hand.PAPER)
        or (my_hand == Hand.PAPER and opponent_hand == Hand.ROCK)
    )


def parse_line(raw_line: str) -> Tuple[Hand, Hand]:
    raw_opponent, raw_player = raw_line.split(" ")
    return opponent_to_hand[raw_opponent], player_to_hand[raw_player]


def test_get_total_score():
    assert (
        get_total_score(
            [
                (Hand.ROCK, Hand.PAPER),
                (Hand.PAPER, Hand.ROCK),
                (Hand.SCISSORS, Hand.SCISSORS),
            ]
        )
        == 15
    )


def test_get_round_score():
    assert get_round_score(Hand.ROCK, Hand.PAPER) == 8
    assert get_round_score(Hand.PAPER, Hand.ROCK) == 1
    assert get_round_score(Hand.SCISSORS, Hand.SCISSORS) == 6


def test_parse_line():
    assert parse_line("A Y") == (Hand.ROCK, Hand.PAPER)


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        rounds = [parse_line(line.rstrip("\n")) for line in f]
    print(get_total_score(rounds))
