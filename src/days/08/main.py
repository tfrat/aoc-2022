from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

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

    def is_out_of_bounds(self, max_x:int, max_y: int) -> bool:
        return self.x < 0 or self.x >= max_x or self.y < 0 or self.y >= max_y


def is_visible(trees: list[list[int]], coord: Coord) -> bool:
    min_max = None
    for direction in Direction:
        next_ = coord.move(direction)
        max_direction = -1
        while not next_.is_out_of_bounds(len(trees), len(trees[0])):
            max_direction = max(max_direction, trees[next_.x][next_.y])
            next_ = next_.move(direction)
        min_max = min(min_max, max_direction) if min_max is not None else max_direction

    return trees[coord.x][coord.y] > min_max


def total_visible_trees(trees: list[list[int]]) -> int:
    total = 0
    for x, row in enumerate(trees_):
        for y, tree in enumerate(row):
            total += 1 if is_visible(trees, Coord(x, y)) else 0

    return total


def calculate_scenic_score(trees: list[list[int]], coord: Coord) -> int:
    tree = trees[coord.x][coord.y]
    score = 1
    for direction in Direction:
        next_ = coord.move(direction)
        direction_score = 0
        while not next_.is_out_of_bounds(len(trees), len(trees[0])):
            direction_score += 1
            if tree <= trees[next_.x][next_.y]:
                break
            next_ = next_.move(direction)
        score *= direction_score

    return score


def highest_scenic_score(trees: list[list[int]]) -> int:
    highest = -1
    for x, row in enumerate(trees_):
        for y, tree in enumerate(row):
            highest = max(highest, calculate_scenic_score(trees, Coord(x, y)))

    return highest


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        trees_ = [[int(tree) for tree in line.rstrip()] for line in f.readlines()]
    start = time.time()
    print(f"Visible trees: {total_visible_trees(trees_)}")
    print(f"Highest Scenic Score: {highest_scenic_score(trees_)}")
    print(f"Time to execute: {time.time() - start}")
