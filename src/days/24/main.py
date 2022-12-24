from __future__ import annotations

import time
from collections import deque
from collections.abc import MutableMapping
from dataclasses import dataclass
from enum import Enum
from typing import Iterator


class Direction(Enum):
    UP = "^"
    LEFT = "<"
    DOWN = "v"
    RIGHT = ">"

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


class BlizzardActivity(MutableMapping[int, set[Blizzard]]):
    store: dict[int, set[Blizzard]]
    width: int
    height: int
    border: set[Coord]

    def __init__(self, width: int, height: int, border: set[Coord]) -> None:
        super().__init__()
        self.store = {}
        self.width = width
        self.height = height
        self.border = border

    def __getitem__(self, minute: int) -> set[Blizzard]:
        if minute not in self.store:
            self.store[minute] = self._move_blizzards(minute - 1)
        return self.store[minute]

    def __setitem__(self, key: int, value: set[Blizzard]) -> None:
        self.store[key] = value

    def __delitem__(self, key: int) -> None:
        del self.store[key]

    def __len__(self) -> int:
        return len(self.store)

    def __iter__(self) -> Iterator[int]:
        return iter(self)

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
                        wrapped_location = Coord(1, next_blizzard.location.y)
                    case Direction.DOWN:
                        wrapped_location = Coord(next_blizzard.location.x, 1)
                    case Direction.LEFT:
                        wrapped_location = Coord(self.width - 2, next_blizzard.location.y)
                    case _:
                        raise ValueError("Unrecognized direction")
                next_blizzard = Blizzard(wrapped_location, next_blizzard.direction)
            moved_blizzards.add(next_blizzard)
        return moved_blizzards

    def blizzards(self, location: Coord, minute: int) -> set[Blizzard]:
        return {blizzard for blizzard in self.get(minute) if blizzard.location == location}


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

    def can_move(self, location: Coord, minute: int) -> bool:
        if location in self.border or location == self.entrance:
            return False
        if location in {blizzard.location for blizzard in self.blizzard_activity[minute]}:
            return False
        return True


def stringify_scene(mountain: Mountain, location: Coord, minute: int) -> str:
    out = ""
    for y in range(mountain.height):
        for x in range(mountain.width):
            pos = Coord(x, y)
            if pos == location:
                out += "E"
            elif pos in mountain.border:
                out += "#"
            elif blizzards := mountain.blizzard_activity.blizzards(pos, minute):
                if len(blizzards) == 1:
                    out += blizzards.pop().direction.value
                else:
                    out += str(len(blizzards))
            else:
                out += "."

        out += "\n"
    return out


def traverse(lines: list[str]) -> int:
    mountain = Mountain(lines)
    location = mountain.entrance
    minutes = 0
    directions = [Direction.DOWN, Direction.RIGHT, None, Direction.UP, Direction.LEFT]
    queue = deque()
    queue.append((location, minutes))
    while location != mountain.exit:
        print(stringify_scene(mountain, location, minutes))
        for direction in directions:
            next_location = location.move(direction) if direction else location
            if mountain.can_move(next_location, minutes + 1):
                break
        minutes += 1
        location = next_location
    return minutes


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    minutes = traverse(lines)
    print(minutes)
    print()


if __name__ == '__main__':
    start = time.time()
    # run("simple_example.txt")
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
