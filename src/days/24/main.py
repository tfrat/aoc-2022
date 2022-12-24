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


class BlizzardActivity(dict[int, set[Blizzard]]):
    width: int
    height: int
    border: set[Coord]

    def __init__(self, width: int, height: int, border: set[Coord]) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.border = border

    def __getitem__(self, minute: int) -> set[Blizzard]:
        if minute not in self:
            self[minute] = self._move_blizzards(minute - 1)
        return self[minute]

    def _move_blizzards(self, minute: int) -> set[Blizzard]:
        blizzards = self.get(minute)
        moved_blizzards = set()
        for blizzard in blizzards:
            next_blizzard = blizzard.move()
            if next_blizzard.location in self.border:
                match next_blizzard.direction:
                    case Direction.UP:
                        wrapped_location = Coord(next_blizzard.location.x, self.height - 2)
                    case Direction.RIGHT:
                        wrapped_location = Coord(2, next_blizzard.location.y)
                    case Direction.DOWN:
                        wrapped_location = Coord(next_blizzard.location.x, 2)
                    case Direction.LEFT:
                        wrapped_location = Coord(self.width - 2, next_blizzard.location.y)
                    case _:
                        raise ValueError("Unrecognized direction")
                next_blizzard = Blizzard(wrapped_location, next_blizzard.direction)
            moved_blizzards.add(next_blizzard)
        return moved_blizzards


class Mountain:
    entrance: Coord
    exit: Coord
    width: int
    height: int
    border: set[Coord]
    blizzards: BlizzardActivity

    def __init__(self, lines: list[str]) -> None:
        self.border = set()
        self.height = len(lines)
        self.width = len(lines[0])
        blizzards = set()
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
                        blizzards.add(Blizzard(Coord(x, y), Direction.from_char(char)))

        # Block the path above the entrance
        self.border.add(Coord(self.entrance.x, self.entrance.y - 1))
        self.blizzard_activity = BlizzardActivity(self.width, self.height, self.border)
        self.blizzard_activity[0] = blizzards


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    mountain = Mountain(lines)
    # solution here
    blizzards = mountain.move_blizzards()
    print()


if __name__ == '__main__':
    start = time.time()
    run("simple_example.txt")
    # run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
