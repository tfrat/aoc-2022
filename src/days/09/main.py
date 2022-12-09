from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "U"
    UP_RIGHT = "UR"
    UP_LEFT = "UL"
    LEFT = "L"
    DOWN = "D"
    DOWN_LEFT = "DOWN_LEFT"
    DOWN_RIGHT = "DOWN_RIGHT"
    RIGHT = "R"


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
            case Direction.UP_LEFT:
                return Coord(self.x - 1, self.y + 1)
            case Direction.LEFT:
                return Coord(self.x - 1, self.y)
            case Direction.DOWN_LEFT:
                return Coord(self.x - 1, self.y - 1)
            case Direction.DOWN:
                return Coord(self.x, self.y - 1)
            case Direction.DOWN_RIGHT:
                return Coord(self.x + 1, self.y - 1)
            case Direction.RIGHT:
                return Coord(self.x + 1, self.y)
            case Direction.UP_RIGHT:
                return Coord(self.x + 1, self.y + 1)

    def is_touching(self, other: Coord) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


@dataclass
class Knot:
    id: int
    position: Coord
    prev: Knot | None = None
    next: Knot | None = None

    def move(self, direction: Direction) -> None:
        self.position = self.position.move(direction)
        if not self.is_tail:
            self.next.follow()

    def follow(self) -> None:
        if not self.is_touching(self.prev):
            prev_pos = self.prev.position
            if prev_pos.x > self.position.x and prev_pos.y > self.position.y:
                self.move(Direction.UP_RIGHT)
            elif prev_pos.x > self.position.x and prev_pos.y < self.position.y:
                self.move(Direction.DOWN_RIGHT)
            elif prev_pos.x < self.position.x and prev_pos.y < self.position.y:
                self.move(Direction.DOWN_LEFT)
            elif prev_pos.x < self.position.x and prev_pos.y > self.position.y:
                self.move(Direction.UP_LEFT)
            elif prev_pos.x > self.position.x:
                self.move(Direction.RIGHT)
            elif prev_pos.x < self.position.x:
                self.move(Direction.LEFT)
            elif prev_pos.y > self.position.y:
                self.move(Direction.UP)
            elif prev_pos.y < self.position.y:
                self.move(Direction.DOWN)
            if not self.is_tail:
                self.next.follow()

    @property
    def is_head(self) -> bool:
        return not bool(self.prev)

    @property
    def is_tail(self) -> bool:
        return not bool(self.next)

    def is_touching(self, knot: Knot) -> bool:
        return self.position.is_touching(knot.position)


class Rope:
    head: Knot
    tail: Knot
    tail_positions: list[Coord]

    def __init__(self, knots: int) -> None:
        self.head = Knot(id=0, position=Coord(0, 0))
        knot = self.head
        for i in range(knots - 1):
            knot.next = Knot(i + 1, Coord(0, 0))
            knot.next.prev = knot
            knot = knot.next
        self.tail = knot
        self.tail_positions = [Coord(0, 0)]

    def move_head(self, direction: Direction, distance: int) -> None:
        for _ in range(distance):
            self.head.move(direction)
            self.tail_positions.append(self.tail.position.copy())

    @property
    def knot_positions(self) -> list[Knot]:
        knots = []
        knot = self.head
        while knot:
            knots.append(knot)
            knot = knot.next
        return knots


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        moves_ = [line.rstrip() for line in f.readlines()]
    start = time.time()
    rope_ = Rope(10)
    for move in moves_:
        direction_, distance_ = move.split()
        rope_.move_head(Direction(direction_), int(distance_))
    unique_positions = len(set(rope_.tail_positions))
    print(f"Unique Tail Position: {unique_positions}")
    print(f"Time to execute: {time.time() - start}")
