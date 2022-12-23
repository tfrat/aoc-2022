from __future__ import annotations

import sys
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"


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

    def neighbors(self, direction: Direction) -> set[Coord]:
        match direction:
            case Direction.UP:
                return {Coord(self.x - 1, self.y - 1), Coord(self.x, self.y - 1), Coord(self.x + 1, self.y - 1)}
            case Direction.DOWN:
                return {Coord(self.x - 1, self.y + 1), Coord(self.x, self.y + 1), Coord(self.x + 1, self.y + 1)}
            case Direction.LEFT:
                return {Coord(self.x - 1, self.y - 1), Coord(self.x - 1, self.y), Coord(self.x - 1, self.y + 1)}
            case Direction.RIGHT:
                return {Coord(self.x + 1, self.y - 1), Coord(self.x + 1, self.y), Coord(self.x + 1, self.y + 1)}

    def touching(self, others: set[Coord]) -> bool:
        neighbors = {
            Coord(self.x + 1, self.y + 1),
            Coord(self.x + 1, self.y - 1),
            Coord(self.x - 1, self.y + 1),
            Coord(self.x - 1, self.y - 1),
            Coord(self.x + 1, self.y),
            Coord(self.x - 1, self.y),
            Coord(self.x, self.y + 1),
            Coord(self.x, self.y - 1),
        }
        return bool(neighbors & others)


@dataclass
class Elf:
    location: Coord
    proposed: Coord | None = None


def bounds(elves: list[Elf]) -> tuple[Coord, Coord]:
    min_x, min_y = sys.maxsize, sys.maxsize
    max_x, max_y = -sys.maxsize, -sys.maxsize
    for elf in elves:
        min_x = min(elf.location.x, min_x)
        min_y = min(elf.location.y, min_y)
        max_x = max(elf.location.x, max_x)
        max_y = max(elf.location.y, max_y)

    return Coord(min_x, min_y), Coord(max_x, max_y)


def grove_dimensions(elves: list[Elf]) -> tuple[int, int]:
    min_pos, max_pos = bounds(elves)
    width = abs(max_pos.x - min_pos.x + 1)
    height = abs(max_pos.y - min_pos.y + 1)
    return width, height


def count_empty_tiles(elves: list[Elf]) -> int:
    width, height = grove_dimensions(elves)
    return width * height - len(elves)


def print_grove(elves: list[Elf]) -> str:
    min_pos, _ = bounds(elves)
    width, height = grove_dimensions(elves)
    out = ""
    positions = {elf.location for elf in elves}
    for y in range(min_pos.y - 1, min_pos.y + height + 1):
        for x in range(min_pos.x - 1, min_pos.x + width + 1):
            position = Coord(x, y)
            if position in positions:
                out += "#"
            else:
                out += "."
        out += "\n"

    return out


def find_elves(lines: list[str]) -> list[Elf]:
    elves = []
    for y, row in enumerate(lines):
        for x, position in enumerate(row):
            if position == "#":
                elves.append(Elf(Coord(x, y)))

    return elves


def move_elves(elves: list[Elf], moves: deque[Direction]) -> tuple[deque[Direction], bool]:
    proposed_moves = defaultdict(lambda: 0)
    current_elf_positions = {elf.location for elf in elves}
    elves_moved = False
    for elf in elves:
        for move in moves:
            if elf.proposed:
                continue

            if not elf.location.touching(current_elf_positions):
                continue

            if elf.location.neighbors(move) & current_elf_positions:
                continue

            elf.proposed = elf.location.move(move)
            proposed_moves[elf.proposed] += 1

    for elf in elves:
        if proposed_moves[elf.proposed] == 1:
            elves_moved = True
            elf.location = elf.proposed
        elf.proposed = None
    next_moves = moves.copy()
    next_moves.rotate(-1)
    return next_moves, elves_moved


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")

    elves = find_elves(lines)
    # print(print_grove(elves))
    moves = deque([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
    keep_moving = True
    count = 0
    while keep_moving:
        moves, keep_moving = move_elves(elves, moves)
        count += 1
        if count == 10:
            print(count_empty_tiles(elves))
        # print(print_grove(elves))

    print(count)

    print()


if __name__ == '__main__':
    start = time.time()
    # run("small_example.txt")
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
