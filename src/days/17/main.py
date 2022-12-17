from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from itertools import cycle


class Direction(Enum):
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def move(self, direction: Direction) -> Coord:
        match direction:
            case Direction.LEFT:
                return Coord(self.x - 1, self.y)
            case Direction.RIGHT:
                return Coord(self.x + 1, self.y)
            case Direction.DOWN:
                return Coord(self.x, self.y - 1)


class Rock(ABC):
    anchor: Coord
    height: int
    positions: set[Coord]
    walls: set[Coord]

    def __init__(self, anchor: Coord, height: int) -> None:
        self.anchor = anchor
        self.height = height
        self.walls = set()
        for offset in range(height):
            self.walls.add(Coord(-1, self.anchor.y + offset))
            self.walls.add(Coord(7, self.anchor.y + offset))

    def __str__(self) -> str:
        return f"{self.__class__}: {self.anchor.x}, {self.anchor.y}"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.anchor)

    @classmethod
    @abstractmethod
    def create(cls, anchor: Coord) -> Rock:
        pass

    def move(self, direction: Direction, collision_map: dict[int, set[Rock]]) -> Rock | None:
        next_position = self.create(self.anchor.move(direction))
        if not self.walls & next_position.positions and next_position.anchor.y >= 0:
            rocks = collision_map[self.anchor.y // 4]
            if not any([rock.will_collide(next_position) for rock in rocks]):
                return next_position
        return None

    def will_collide(self, other: Rock) -> bool:
        return bool(self.positions & other.positions)


class HorizontalRock(Rock):
    def __init__(self, anchor: Coord) -> None:
        super().__init__(anchor, 1)
        self.positions = {
            self.anchor,
            Coord(self.anchor.x + 1, self.anchor.y),
            Coord(self.anchor.x + 2, self.anchor.y),
            Coord(self.anchor.x + 3, self.anchor.y)
        }

    @classmethod
    def create(cls, anchor: Coord) -> Rock:
        return HorizontalRock(anchor)


class VerticalRock(Rock):
    def __init__(self, anchor: Coord) -> None:
        super().__init__(anchor, 4)
        self.positions = {
            self.anchor,
            Coord(self.anchor.x, self.anchor.y + 1),
            Coord(self.anchor.x, self.anchor.y + 2),
            Coord(self.anchor.x, self.anchor.y + 3)
        }

    @classmethod
    def create(cls, anchor: Coord) -> Rock:
        return VerticalRock(anchor)


class PlusRock(Rock):
    def __init__(self, anchor: Coord) -> None:
        super().__init__(anchor, 3)
        self.positions = {
            Coord(self.anchor.x + 1, self.anchor.y),
            Coord(self.anchor.x, self.anchor.y + 1),
            Coord(self.anchor.x + 1, self.anchor.y + 1),
            Coord(self.anchor.x + 1, self.anchor.y + 2),
            Coord(self.anchor.x + 2, self.anchor.y + 1),
        }

    @classmethod
    def create(cls, anchor: Coord) -> Rock:
        return PlusRock(anchor)


class SquareRock(Rock):
    def __init__(self, anchor: Coord) -> None:
        super().__init__(anchor, 2)
        self.positions = {
            self.anchor,
            Coord(self.anchor.x, self.anchor.y + 1),
            Coord(self.anchor.x + 1, self.anchor.y),
            Coord(self.anchor.x + 1, self.anchor.y + 1),
        }

    @classmethod
    def create(cls, anchor: Coord) -> Rock:
        return SquareRock(anchor)


class ReverseLRock(Rock):
    def __init__(self, anchor: Coord) -> None:
        super().__init__(anchor, 3)
        self.positions = {
            self.anchor,
            Coord(self.anchor.x + 1, self.anchor.y),
            Coord(self.anchor.x + 2, self.anchor.y),
            Coord(self.anchor.x + 2, self.anchor.y + 1),
            Coord(self.anchor.x + 2, self.anchor.y + 2),
        }

    @classmethod
    def create(cls, anchor: Coord) -> Rock:
        return ReverseLRock(anchor)


def draw_cave(collision_map: dict[int, set[Rock]], height: int, falling_rock: Rock | None = None) -> str:
    if falling_rock:
        height = max(height, falling_rock.height + falling_rock.anchor.y)
    cave = [["." for _ in range(7)] for _ in range(height)]
    for rocks in collision_map.values():
        for rock in rocks:
            for position in rock.positions:
                cave[position.y][position.x] = "#"
    if falling_rock:
        for position in falling_rock.positions:
            cave[position.y][position.x] = "@"
    out = ""
    for i, row in enumerate(cave[::-1]):
        out += f"{i:04d} |"
        for position in row:
            out += position
        out += "|\n"
    out += "=" * 9
    return out


def drop_rocks(jetstream: list[Direction], rock_count: int) -> tuple[int, list]:
    rock_order = [HorizontalRock, PlusRock, ReverseLRock, VerticalRock, SquareRock]
    rock_cycle = cycle(rock_order)
    jetstream_cycle = cycle(jetstream)
    collision_map = defaultdict(set)
    height = -1
    falling_rock = next(rock_cycle)(Coord(2, 3))
    steps = []
    for _ in range(rock_count):
        falling = True
        down_toggle = False
        steps.append((draw_cave(collision_map, height, falling_rock), None, height))
        while falling:
            if down_toggle:
                direction = Direction.DOWN
            else:
                direction = next(jetstream_cycle)
            down_toggle = not down_toggle
            # steps.append((draw_cave(collision_map, height, falling_rock), direction, height))
            if next_rock := falling_rock.move(direction, collision_map):
                falling_rock = next_rock
            elif direction == Direction.DOWN:
                falling = False
        collision_map[falling_rock.anchor.y // 4].add(falling_rock)
        collision_map[(falling_rock.anchor.y + falling_rock.height) // 4].add(falling_rock)
        height = max(height, falling_rock.anchor.y + falling_rock.height)
        steps.append((draw_cave(collision_map, height), None, height))
        falling_rock = next(rock_cycle)(Coord(2, height + 3))
    # steps.append((draw_cave(collision_map, height), None, height))
    return height, steps


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        jetstream = [Direction.LEFT if char == "<" else Direction.RIGHT for char in f.readline().rstrip()]
    print(f"File: {filename}")
    rock_total = 100
    final_height, steps = drop_rocks(jetstream, rock_total)
    out_str = "".join([step[0] + "\n" + str(step[1]) + f", {step[2]}" + "\n\n" for step in steps])
    with open(f"steps-{rock_total}.txt", "w", encoding="utf-8") as f:
        f.write(out_str)
    print(final_height)
    # solution here

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
