from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)


def get_dimensions(coords: list[Coord]) -> tuple[int, int, int]:
    max_width, max_height, max_depth = 0, 0, 0
    for coord in coords:
        max_width = max(max_width, coord.x)
        max_height = max(max_height, coord.y)
        max_depth = max(max_depth, coord.z)
    return max_width, max_height, max_depth


class LavaDropletScan:
    grid: list[list[list[bool]]]
    coords: set[Coord]
    width: int
    height: int
    depth: int
    neighbors: list[Coord] = [
        Coord(0, 0, 1),
        Coord(0, 0, -1),
        Coord(0, 1, 0),
        Coord(0, -1, 0),
        Coord(1, 0, 0),
        Coord(-1, 0, 0),
    ]

    def __init__(self, coords: list[Coord]) -> None:
        self.width, self.height, self.depth = get_dimensions(coords)
        self.coords = set(coords)
        self.grid = [
            [
                [
                    False for _ in range(self.depth + 1)
                ] for _ in range(self.height + 1)
            ] for _ in range(self.width + 1)
        ]
        for coord in coords:
            self.grid[coord.x][coord.y][coord.z] = True

    def has_cube(self, coord: Coord) -> bool:
        if 0 <= coord.x <= self.width and 0 <= coord.y <= self.height and 0 <= coord.z <= self.depth:
            return self.grid[coord.x][coord.y][coord.z]
        return False

    @property
    def surface_area(self) -> int:
        total = 0
        for coord in self.coords:
            surface_area = 6
            for neighbor in self.neighbors:
                if self.has_cube(coord + neighbor):
                    surface_area -= 1
            total += surface_area

        return total

    @property
    def reachable_surface_area(self) -> int:
        unreachable_area = 0
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    location = Coord(x, y, z)
                    if location not in self.coords:
                        sides_touched = 0
                        for neighbor in self.neighbors:
                            if self.has_cube(location + neighbor):
                                sides_touched += 1
                        if sides_touched == 6:
                            unreachable_area += sides_touched
        return self.surface_area - unreachable_area


def run(filename: str) -> None:
    print(f"File: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        lines = [(int(value) for value in line.rstrip().split(",")) for line in f.readlines()]

    coords = [Coord(*values) for values in lines]
    grid = LavaDropletScan(coords)
    print(grid.surface_area)
    print(grid.reachable_surface_area)

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    # too high 4178
    print(f"Time to execute: {time.time() - start}")
