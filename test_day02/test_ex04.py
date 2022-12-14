from pathlib import Path
from typing import Dict, Tuple, Iterable, List
from enum import StrEnum, auto


class Hand(StrEnum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


class Result(StrEnum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


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

player_to_result: Dict[str, Result] = {
    "X": Result.LOSE,
    "Y": Result.DRAW,
    "Z": Result.WIN,
}


def get_total_score(rounds: Iterable[Tuple[Hand, Result]]):
    return sum(get_round_score(*hands) for hands in rounds)


def get_round_score(opponent_hand: Hand, result: Result) -> int:
    outcome_score = 0
    if result == result.DRAW:
        outcome_score = 3
    elif result == result.WIN:
        outcome_score = 6
    my_hand = get_my_hand(opponent_hand, result)
    return outcome_score + shape_score[my_hand]


def get_my_hand(opponent_hand: Hand, result: Result) -> Hand:
    hands_list: List[Hand] = list(Hand)
    opponent_index = hands_list.index(opponent_hand)
    if result == result.DRAW:
        return opponent_hand
    elif result == result.LOSE:
        return hands_list[opponent_index - 1]
    else:
        return hands_list[0 if opponent_index == 2 else opponent_index + 1]


def parse_line(raw_line: str) -> Tuple[Hand, Result]:
    raw_opponent, raw_player = raw_line.split(" ")
    return opponent_to_hand[raw_opponent], player_to_result[raw_player]


def test_get_total_score():
    assert (
        get_total_score(
            [
                (Hand.ROCK, Result.DRAW),
                (Hand.PAPER, Result.LOSE),
                (Hand.SCISSORS, Result.WIN),
            ]
        )
        == 12
    )


def test_get_round_score():
    assert get_round_score(Hand.ROCK, Result.DRAW) == 4
    assert get_round_score(Hand.PAPER, Result.LOSE) == 1
    assert get_round_score(Hand.SCISSORS, Result.WIN) == 7


def test_parse_line():
    assert parse_line("A Y") == (Hand.ROCK, Result.DRAW)


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        rounds = [parse_line(line.rstrip("\n")) for line in f]
    print(get_total_score(rounds))
