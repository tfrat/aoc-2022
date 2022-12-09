from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum, auto


class Direction(Enum):
    UP = "U"
    LEFT = "L"
    DOWN = "D"
    RIGHT = "R"


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def move(self, direction: Direction) -> Coord:
        match direction:
            case Direction.UP:
                return Coord(self.x, self.y + 1)
            case Direction.DOWN:
                return Coord(self.x, self.y - 1)
            case Direction.LEFT:
                return Coord(self.x - 1, self.y)
            case Direction.RIGHT:
                return Coord(self.x + 1, self.y)

    def is_out_of_bounds(self, max_x:int, max_y: int) -> bool:
        return self.x < 0 or self.x >= max_x or self.y < 0 or self.y >= max_y

    def is_touching(self, other: Coord) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


def execute_move_list(moves: list[str]) -> list[Coord]:
    head = Coord(0, 0)
    tail = Coord(0, 0)
    positions = [tail]
    for move in moves:
        direction = Direction(move.split()[0])
        distance = int(move.split()[1])
        for _ in range(distance):
            old = head
            head = head.move(direction)
            foo = f"head: {head}"
            if not head.is_touching(tail):
                tail = old
                positions.append(tail)
                foo += f", tail: {tail}"
            print(foo)

    return positions


if __name__ == '__main__':
    with open("example.txt", "r", encoding="utf-8") as f:
        moves_ = [line.rstrip() for line in f.readlines()]
    start = time.time()

    tail_positions = execute_move_list(moves_)
    print(tail_positions)
    print(f"The tail reached {len(set(tail_positions))} positions")

    print(f"Time to execute: {time.time() - start}")
