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

    @classmethod
    @abstractmethod
    def create(cls, anchor: Coord) -> Rock:
        pass

    def move(self, direction: Direction, collision_map: dict[int, list[Rock]]) -> Rock | None:
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


def drop_rocks(jetstream: list[Direction], rock_count: int) -> int:
    rock_order = [HorizontalRock, PlusRock, ReverseLRock, VerticalRock, SquareRock]
    rock_cycle = cycle(rock_order)
    jetstream_cycle = cycle(jetstream)
    collision_map = defaultdict(list)
    height = -1
    falling_rock = next(rock_cycle)(Coord(2, 3))
    for _ in range(rock_count):
        falling = True
        down_toggle = False
        while falling:
            direction = Direction.DOWN if down_toggle else next(jetstream_cycle)
            down_toggle = not down_toggle
            if next_rock := falling_rock.move(direction, collision_map):
                falling_rock = next_rock
            elif direction == Direction.DOWN:
                falling = False
        collision_map[falling_rock.anchor.y // 4].append(falling_rock)
        height = max(height, falling_rock.anchor.y + falling_rock.height)
        falling_rock = next(rock_cycle)(Coord(2, height + 3))

    return height


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        jetstream = [Direction.LEFT if char == "<" else Direction.RIGHT for char in f.readline().rstrip()]
    print(f"File: {filename}")
    print(drop_rocks(jetstream, 2022))
    # solution here

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
