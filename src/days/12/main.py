from __future__ import annotations

import sys
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


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
    width: int
    height: int

    def __init__(self, elevations: list[list[int]]) -> None:
        self.elevations = elevations
        self.width = len(self.elevations)
        self.height = len(self.elevations[0])

    def is_in(self, coord: Coord) -> bool:
        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    def can_step(self, start: Coord, end: Coord) -> bool:
        if not self.is_in(end):
            return False

        return self.get_elevation(start) >= self.get_elevation(end) - 1

    def get_elevation(self, coord: Coord) -> int:
        if self.is_in(coord):
            return self.elevations[coord.x][coord.y]
        return -1

    def find_shortest_path(self, start: Coord, target: Coord) -> int:
        queue = deque()
        queue.append((start, 0))
        memo = [[-1 for _ in range(self.height)] for _ in range(self.width)]
        while queue:
            current, steps = queue.popleft()
            if memo[current.x][current.y] != -1:
                continue

            memo[current.x][current.y] = (current, steps)

            for direction in Direction:
                next_coord = current.move(direction)
                if self.can_step(current, next_coord):
                    queue.append((next_coord, steps + 1))
        return memo[target.x][target.y]


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


def find_all_starts(grid: Grid) -> list[Coord]:
    starts = []
    for x, row in enumerate(grid.elevations):
        for y, value in enumerate(row):
            if value == 1:
                starts.append(Coord(x, y))

    return starts


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


def run() -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    grid, start, end = create_grid(lines)
    print(f"Part 1: {grid.find_shortest_path(start, end)}")

    starts = find_all_starts(grid)
    shortest_paths = filter(lambda x: x != -1, [grid.find_shortest_path(start, end) for start in starts])
    print(f"Part 2: {min(shortest_paths)}")


if __name__ == '__main__':
    start_time = time.time()
    run()
    print(f"Time to execute: {time.time() - start_time}")
