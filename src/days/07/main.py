from __future__ import annotations
from dataclasses import dataclass, field
from itertools import chain


@dataclass
class Directory:
    parent: Directory | None = None
    directories: dict[str, Directory] = field(default_factory=dict)
    files: dict[str, int] = field(default_factory=dict)
    total_size: int = 0

    def add_directory(self, name: str) -> None:
        self.directories[name] = Directory(parent=self)

    def add_file(self, name: str, size: int) -> None:
        self.files[name] = size
        self.update_size(size)

    def update_size(self, size: int) -> None:
        self.total_size += size
        if self.parent:
            self.parent.update_size(size)


def process_lines(command: str, lines: list[str], current: Directory) -> None:
    match command.split():
        case ["$", "cd", "/"]:
            d = current
            while d.parent:
                d = d.parent
            return process_lines(lines[0], lines[1:], d)
        case ["$", "cd", ".."]:
            return process_lines(lines[0], lines[1:], current.parent)
        case ["$",  "cd", target_dir]:
            return process_lines(lines[0], lines[1:], current.directories[target_dir])
        case ["$", "ls"]:
            for index, line in enumerate(lines):
                if line.startswith("$"):
                    return process_lines(lines[index], lines[index+1:], current)
                match line.split():
                    case ["dir", name]:
                        current.add_directory(name)
                    case [size, name]:
                        current.add_file(name, int(size))
        case _:
            raise ValueError(f"Command not recognized: {command}")


def sum_directories_under_limit(directory: Directory, limit: int) -> int:
    size = directory.total_size if directory.total_size <= limit else 0
    return size + sum([sum_directories_under_limit(child, limit) for child in directory.directories.values()])


def find_directories_to_delete(current: Directory, needed_space: int) -> list[int]:
    sizes = [current.total_size] if current.total_size >= needed_space else []
    sizes += list(chain(*[find_directories_to_delete(child, needed_space) for child in current.directories.values()]))
    return sizes


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        lines_ = [line.rstrip() for line in f.readlines()]

    root = Directory()
    process_lines(lines_[0], lines_[1:], root)
    print(sum_directories_under_limit(root, 100000))
    free_space = (70000000 - root.total_size)
    needed_space_ = 30000000 - free_space
    print(min(find_directories_to_delete(root, needed_space_)))
