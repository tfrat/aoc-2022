from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class Material(Enum):
    AIR = "."
    STONE = "#"
    SAND = "o"
    VOID = "~"


@dataclass
class Coord:
    x: int
    y: int

    def move(self, direction: Coord) -> Coord:
        return Coord(self.x + direction.x, self.y + direction.y)


@dataclass
class Cave:
    top_right: Coord
    bottom_left: Coord
    grid: list[list[Material]]

    def __init__(self, structures: list[list[Coord]]) -> None:
        coords = []
        for structure in structures:
            coords.extend(structure)
        self.top_right = Coord(max(*coords, key=lambda coord: coord.x).x, 0)
        self.bottom_left = Coord(min(*coords, key=lambda coord: coord.x).x, max(*coords, key=lambda coord: coord.y).y)

        self.grid = []
        for _ in range(self.bottom_left.y + 1 + 2):
            self.grid.append([Material.AIR for _ in range(self.top_right.x * 2 + 1)])

        for structure in structures:
            for first, second in zip(structure, structure[1:]):
                if first.x != second.x:
                    for x in range(min(first.x, second.x), max(first.x, second.x) + 1):
                        self._set_material(Coord(x, first.y), Material.STONE)
                else:
                    for y in range(min(first.y, second.y), max(first.y, second.y) + 1):
                        self._set_material(Coord(first.x, y), Material.STONE)

        for x in range(len(self.grid[0])):
            self._set_material(Coord(x, len(self.grid) - 1), Material.STONE)

    def _set_material(self, coord: Coord, material: Material) -> None:
        self.grid[coord.y][coord.x] = material

    def _get_material(self, coord: Coord) -> Material:
        # Enable for VOID
        # if not self.bottom_left.x <= coord.x <= self.top_right.x or not self.top_right.y <= coord.y <= self.bottom_left.y:
        #     return Material.VOID
        return self.grid[coord.y][coord.x]

    def __str__(self) -> str:
        out = ""
        for row in self.grid:
            for material in row:
                out += material.value
            out += "\n"
        return out

    def drop_sand(self, source: Coord) -> bool:
        directions = [Coord(0, 1), Coord(-1, 1), Coord(1, 1)]
        current = source
        can_move = True
        while can_move:
            can_move = False
            for direction in directions:
                if self._get_material(current.move(direction)) == Material.VOID:
                    return False

                if self._get_material(current.move(direction)) == Material.AIR:
                    current = current.move(direction)
                    can_move = True
                    break
        self._set_material(current, Material.SAND)
        if current == source:
            return False
        return True


def parse_structure(lines: list[str]) -> list[list[Coord]]:
    structures = []
    for line in lines:
        structures.append([Coord(int(coord.split(",")[0]), int(coord.split(",")[1])) for coord in line.split(" -> ")])

    return structures


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")

    coords = parse_structure(lines)
    cave = Cave(coords)
    count = 1
    while cave.drop_sand(Coord(500, 0)):
        count += 1
    print(count)
    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
