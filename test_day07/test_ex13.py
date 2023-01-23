from pathlib import Path
from dataclasses import dataclass
from typing import Iterable

from more_itertools import split_before


@dataclass(frozen=True)
class Command:
    instrucion: str
    output: list[str]


@dataclass(frozen=True)
class File:
    name: str
    size: int
    parent: "Folder"


@dataclass(frozen=True)
class Folder:
    name: str
    files: dict[str, File]
    folders: dict[str, "Folder"]
    parent: "Folder | None"

    @staticmethod
    def create_empty(name: str, parent: "Folder | None" = None) -> "Folder":
        return Folder(name, {}, {}, parent)

    @property
    def size(self) -> int:
        return sum(
            item.size
            for item in list(self.files.values()) + list(self.folders.values())
        )


def execute_commands(commands: list[Command]) -> Folder:
    tree = Folder.create_empty("/")
    actual = tree
    for command in commands[1:]:
        if command.instrucion == "ls":
            for item in command.output:
                if item.startswith("dir"):
                    name = item.split()[1]
                    actual.folders[name] = Folder.create_empty(name, actual)
                else:
                    raw_size, name = item.split()
                    actual.files[name] = File(name, int(raw_size), actual)
        else:
            folder_name = command.instrucion.split()[1]
            if folder_name == "..":
                actual = actual.parent  # type: ignore
            else:
                actual = actual.folders[folder_name]
    return tree


def parse_lines_to_commands(lines: Iterable[str]) -> list[Command]:
    return [
        Command(group[0].strip("$ "), group[1:])
        for group in split_before(lines, lambda line: line[0] == "$")
    ]


def get_sum_of_sizes_with_max_size(tree: Folder, max_size: int = 100000) -> int:
    sum_of_sizes = tree.size if tree.size <= max_size else 0
    for folder in tree.folders.values():
        sum_of_sizes += get_sum_of_sizes_with_max_size(folder, max_size)
    return sum_of_sizes


def test_parse_lines_to_commands():
    assert parse_lines_to_commands(
        [
            "$ cd /",
            "$ ls",
            "14848514 b.txt",
            "$ cd a",
            "$ ls",
            "dir e",
            "29116 f",
        ]
    ) == [
        Command("cd /", []),
        Command("ls", ["14848514 b.txt"]),
        Command("cd a", []),
        Command("ls", ["dir e", "29116 f"]),
    ]


def test_execute_commands():
    tree = execute_commands(
        [
            Command("cd /", []),
            Command("ls", ["dir a", "123 b.txt", "dir c"]),
            Command("cd a", []),
            Command("ls", ["456 d.txt"]),
            Command("cd ..", []),
            Command("cd c", []),
            Command("ls", ["789 e.txt"]),
        ]
    )
    assert tree.name == "/"
    assert tree.folders["c"].name == "c"
    assert tree.folders["a"].files["d.txt"].size == 456


def test_folder_size():
    tree = execute_commands(
        [
            Command("cd /", []),
            Command("ls", ["dir a"]),
            Command("cd a", []),
            Command("ls", ["100 b.txt", "dir c"]),
            Command("cd c", []),
            Command("ls", ["100 d.txt", "100 e.txt"]),
        ]
    )
    assert tree.name == "/"
    assert tree.folders["a"].size == 300


def test_get_sum_of_sizes_with_max_size():
    tree = execute_commands(
        parse_lines_to_commands(
            [
                "$ cd /",
                "$ ls",
                "dir a",
                "14848514 b.txt",
                "8504156 c.dat",
                "dir d",
                "$ cd a",
                "$ ls",
                "dir e",
                "29116 f",
                "2557 g",
                "62596 h.lst",
                "$ cd e",
                "$ ls",
                "584 i",
                "$ cd ..",
                "$ cd ..",
                "$ cd d",
                "$ ls",
                "4060174 j",
                "8033020 d.log",
                "5626152 d.ext",
                "7214296 k",
            ]
        )
    )
    assert get_sum_of_sizes_with_max_size(tree, 100000) == 95437


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
    tree = execute_commands(parse_lines_to_commands(lines))
    print(get_sum_of_sizes_with_max_size(tree))
