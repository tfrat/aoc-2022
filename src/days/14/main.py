from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class Material(Enum):
    AIR = "."
    STONE = "#"
    SAND = "o"


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Cave:
    top_right: Coord
    bottom_left: Coord
    horizontal_offset: int
    sand_source: Coord
    grid: list[list[Material]]

    def __init__(self, structures: list[list[Coord]], sand_source: Coord = Coord(500, 0)) -> None:
        self.sand_source = sand_source
        coords = []
        for structure in structures:
            coords.extend(structure)
        self.top_right = Coord(max(*coords, key=lambda coord: coord.x).x, 0)
        self.bottom_left = Coord(min(*coords, key=lambda coord: coord.x).x, max(*coords, key=lambda coord: coord.y).y)
        self.horizontal_offset = self.bottom_left.x

        self.grid = []
        for _ in range(self.bottom_left.y + 1):
            self.grid.append([Material.AIR for _ in range(self.top_right.x - self.bottom_left.x + 1)])

        for structure in structures:
            for first, second in zip(structure, structure[1:]):
                if first.x != second.x:
                    for x in range(min(first.x, second.x), max(first.x, second.x) + 1):
                        self._set_material(Coord(x, first.y), Material.STONE)
                else:
                    for y in range(min(first.y, second.y), max(first.y, second.y) + 1):
                        self._set_material(Coord(first.x, y), Material.STONE)

    def _set_material(self, coord: Coord, material: Material) -> None:
        self.grid[coord.y][coord.x - self.horizontal_offset] = material

    def __str__(self) -> str:
        out = ""
        for row in self.grid:
            for material in row:
                out += material.value
            out += "\n"
        return out


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
    print(cave)
    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
