from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"

    @staticmethod
    def from_char(char: str) -> Direction:
        match char:
            case "<":
                return Direction.LEFT
            case ">":
                return Direction.RIGHT
            case "^":
                return Direction.UP
            case "v":
                return Direction.DOWN
            case _:
                raise ValueError(f"Not a valid direction: {char}")



@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def move(self, direction: Direction) -> Coord:
        match direction:
            case Direction.UP:
                return Coord(self.x, self.y - 1)
            case Direction.DOWN:
                return Coord(self.x, self.y + 1)
            case Direction.LEFT:
                return Coord(self.x - 1, self.y)
            case Direction.RIGHT:
                return Coord(self.x + 1, self.y)


@dataclass(frozen=True)
class Blizzard:
    location: Coord
    direction: Direction

    def move(self) -> Blizzard:
        return Blizzard(self.location.move(self.direction), self.direction)


class Mountain:
    entrance: Coord
    exit: Coord
    border: set[Coord]
    blizzards: set[Blizzard]

    def __init__(self, lines: list[str]) -> None:
        self.border = set()
        self.blizzards = set()
        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                match char:
                    case "#":
                        self.border.add(Coord(x, y))
                    case ".":
                        if y == 0:
                            self.entrance = Coord(x, y)
                        if y == len(lines) - 1:
                            self.exit = Coord(x, y)
                    case "^" | "v" | "<" | ">":
                        self.blizzards.add(Blizzard(Coord(x, y), Direction.from_char(char)))

        # Block the path above the entrance
        self.border.add(Coord(self.entrance.x, self.entrance.y - 1))


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    mountain = Mountain(lines)
    # solution here

    print()


if __name__ == '__main__':
    start = time.time()
    run("simple_example.txt")
    # run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
