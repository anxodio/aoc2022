from pathlib import Path

from more_itertools import sliding_window


def get_start_of_packet_index(datastream: str) -> int:
    for i, chars in enumerate(sliding_window(datastream, 4), 4):
        if len(chars) == len(set(chars)):
            return i
    raise Exception("Start of packet not found :(")


def test_get_start_of_packet_index():
    assert get_start_of_packet_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert get_start_of_packet_index("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert get_start_of_packet_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        datastream = [line.rstrip("\n") for line in f][0]
    print(get_start_of_packet_index(datastream))
