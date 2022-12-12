from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final


def print_grid(grid: list[list[Any]]) -> None:
    out = ""
    for line in grid:
        out += "| "
        for value in line:
            if isinstance(value, int) and 0 <= value <= 9:
                out += " "
            out += str(value) + " | "
        out += "\n"

    print(out)


class Direction(Enum):
    UP = "U"
    LEFT = "L"
    DOWN = "D"
    RIGHT = "R"

    @property
    def opposite(self) -> Direction:
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.DOWN:
                return Direction.UP


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def copy(self) -> Coord:
        return Coord(self.x, self.y)

    def move(self, direction: Direction) -> Coord:
        match direction:
            case Direction.UP:
                return Coord(self.x, self.y + 1)
            case Direction.LEFT:
                return Coord(self.x - 1, self.y)
            case Direction.DOWN:
                return Coord(self.x, self.y - 1)
            case Direction.RIGHT:
                return Coord(self.x + 1, self.y)


@dataclass
class Grid:
    elevations: list[list[int]]
    memo: list[list[int]]
    visited: set[Coord]
    high_value: Final[int] = sys.maxsize

    def __init__(self, elevations: list[list[int]]) -> None:
        self.elevations = elevations
        self.memo = [[-1 for _ in range(len(elevations[0]))] for _ in range(len(elevations))]
        self.visited = set()

    def is_in(self, coord: Coord) -> bool:
        width = len(self.elevations)
        height = len(self.elevations[0])
        return coord.x >= 0 and coord.y >= 0 and coord.x < width and coord.y < height

    def can_step(self, start: Coord, end: Coord) -> bool:
        if not self.is_in(start) or not self.is_in(end) or end in self.visited:
            return False

        # return self.get_elevation(start) in {self.get_elevation(end), self.get_elevation(end) - 1}
        return self.get_elevation(start) >= self.get_elevation(end) - 1

    def get_elevation(self, coord: Coord) -> int:
        if self.is_in(coord):
            return self.elevations[coord.x][coord.y]
        return -1

    def set_memo(self, coord: Coord, value: int) -> int:
        self.memo[coord.x][coord.y] = value
        return value

    def get_memo(self, coord: Coord) -> int:
        if self.is_in(coord):
            return self.memo[coord.x][coord.y]
        return -1

    def find_shortest_path(self, steps: int, start: Coord, end: Coord) -> int:
        if start == end:
            return steps

        if (memo := self.get_memo(start)) != -1:
            return memo + 1

        self.visited.add(start)

        possible_steps = []
        for direction in Direction:
            next_coord = start.move(direction)
            if self.can_step(start, next_coord):
                possible_steps.append(self.find_shortest_path(next_coord, end))

        self.visited.remove(start)

        if not possible_steps:
            return self.high_value
        return 1 + self.set_memo(start, min(possible_steps))


def create_grid(lines: list[str]) -> Grid:
    values = [[None for _ in range(len(lines[0]))] for _ in range(len(lines))]
    start = None
    end = None
    for x, line in enumerate(lines):
        for y, value in enumerate(line):
            if value == "S":
                int_value = 1
                start = Coord(x, y)
            elif value == "E":
                int_value = 26
                end = Coord(x, y)
            else:
                int_value = ord(value) - ord("a") + 1
            values[x][y] = int_value

    if start is None or end is None:
        raise ValueError("No start or end specified")

    return Grid(values), start, end



def run() -> None:
    with open("example.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    grid, start, end = create_grid(lines)
    shortest_path = grid.find_shortest_path(start, end)
    print(shortest_path)
    print_grid(grid.memo)
    print_grid(grid.elevations)


if __name__ == '__main__':
    start_time = time.time()
    run()
    print(f"Time to execute: {time.time() - start_time}")
