from pathlib import Path

from more_itertools import sliding_window


def get_start_of_message_index(datastream: str) -> int:
    for i, chars in enumerate(sliding_window(datastream, 14), 14):
        if len(chars) == len(set(chars)):
            return i
    raise Exception("Start of packet not found :(")


def test_get_start_of_message_index():
    assert get_start_of_message_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert get_start_of_message_index("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert get_start_of_message_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        datastream = [line.rstrip("\n") for line in f][0]
    print(get_start_of_message_index(datastream))
