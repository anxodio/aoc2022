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


def get_directory_to_delete_size(
    tree: Folder, fs_size: int = 70000000, min_unused_space: int = 30000000
) -> int:
    min_file_size = min_unused_space - (fs_size - tree.size)
    return min(_get_directories_to_delete_sizes(tree, min_file_size))


def _get_directories_to_delete_sizes(tree: Folder, min_file_size: int) -> list[int]:
    to_delete_sizes = [tree.size] if tree.size >= min_file_size else []
    for folder in tree.folders.values():
        to_delete_sizes += _get_directories_to_delete_sizes(folder, min_file_size)
    return to_delete_sizes


def test_get_directory_to_delete():
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
    assert get_directory_to_delete_size(tree, 70000000, 30000000) == 24933642


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
    tree = execute_commands(parse_lines_to_commands(lines))
    print(get_directory_to_delete_size(tree))
