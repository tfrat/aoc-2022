from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum, auto


class Material(Enum):
    EXTERIOR = auto()
    LAVA = auto()
    INTERIOR = auto()


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self) -> str:
        return f"{self.x}, {self.y}, {self.z}"

def get_dimensions(coords: list[Coord]) -> tuple[int, int, int]:
    max_width, max_height, max_depth = 0, 0, 0
    for coord in coords:
        max_width = max(max_width, coord.x)
        max_height = max(max_height, coord.y)
        max_depth = max(max_depth, coord.z)
    return max_width, max_height, max_depth


class LavaDropletScan:
    grid: list[list[list[Material]]]
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
                    Material.EXTERIOR for _ in range(self.depth + 1)
                ] for _ in range(self.height + 1)
            ] for _ in range(self.width + 1)
        ]
        for coord in coords:
            self.grid[coord.x][coord.y][coord.z] = Material.LAVA
        visited = [
            [
                [
                    False for _ in range(self.depth + 1)
                ] for _ in range(self.height + 1)
            ] for _ in range(self.width + 1)
        ]
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    coord = Coord(x, y, z)
                    if not visited[coord.x][coord.y][coord.z] and self.is_enclosed(coord, visited):
                        self.set_enclosed(coord)

    def is_enclosed(self, coord: Coord, visited: list[list[list[bool]]]) -> bool:
        stack = list()
        stack.append(coord)

        enclosed = True
        while stack:
            current = stack.pop()

            if not self.in_bounds(coord):
                enclosed = False
                continue

            if visited[coord.x][coord.y][coord.z] or self.get_material(coord) == Material.LAVA:
                continue
            visited[coord.x][coord.y][coord.z] = True

            for neighbor in self.neighbors:
                stack.append(current + neighbor)

        return enclosed

    def set_enclosed(self, coord: Coord) -> None:
        stack = list()
        stack.append(coord)

        while stack:
            current = stack.pop()

            if self.get_material(coord) in {Material.LAVA, Material.INTERIOR}:
                continue

            self.grid[coord.x][coord.y][coord.z] = Material.INTERIOR

            for neighbor in self.neighbors:
                stack.append(current + neighbor)

    def in_bounds(self, coord: Coord) -> bool:
        return 0 <= coord.x <= self.width and 0 <= coord.y <= self.height and 0 <= coord.z <= self.depth

    def get_material(self, coord: Coord) -> Material:
        if self.in_bounds(coord):
            return self.grid[coord.x][coord.y][coord.z]
        return Material.EXTERIOR

    @property
    def surface_area(self) -> int:
        total = 0
        for coord in self.coords:
            surface_area = 6
            for neighbor in self.neighbors:
                if self.get_material(coord + neighbor) in {Material.LAVA, Material.INTERIOR}:
                    surface_area -= 1
            total += surface_area

        return total


def run(filename: str) -> None:
    print(f"File: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        lines = [(int(value) for value in line.rstrip().split(",")) for line in f.readlines()]

    coords = [Coord(*values) for values in lines]
    grid = LavaDropletScan(coords)
    print(grid.surface_area)

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    # too high 4178
    print(f"Time to execute: {time.time() - start}")
