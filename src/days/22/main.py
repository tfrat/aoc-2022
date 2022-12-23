from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from itertools import zip_longest


class Material(Enum):
    VOID = "void"
    WALL = "wall"
    PATH = "path"


class Turn(Enum):
    LEFT = "left"
    RIGHT = "right"


class Orientation(Enum):
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"

    def points(self) -> int:
        match self:
            case Orientation.RIGHT:
                return 0
            case Orientation.DOWN:
                return 1
            case Orientation.LEFT:
                return 2
            case Orientation.UP:
                return 3

    def turn(self, turn: Turn):
        orientations = [
            Orientation.UP,
            Orientation.RIGHT,
            Orientation.DOWN,
            Orientation.LEFT,
        ]
        index = orientations.index(self)
        move = 1 if turn == Turn.RIGHT else -1
        return orientations[(index + move) % len(orientations)]


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def move(self, direction: Orientation) -> Coord:
        match direction:
            case Orientation.UP:
                return Coord(self.x, self.y - 1)
            case Orientation.RIGHT:
                return Coord(self.x + 1, self.y)
            case Orientation.DOWN:
                return Coord(self.x, self.y + 1)
            case Orientation.LEFT:
                return Coord(self.x - 1, self.y)


class Map:
    _grid: list[list[Material]]
    height: int
    width: int

    def __init__(self, lines: list[str]) -> None:
        self.height = len(lines)
        self.width = max(len(row) for row in lines)
        self._grid = [[Material.VOID for x in range(self.width)] for y in range(self.height)]
        for y, row in enumerate(lines):
            for x, value in enumerate(row):
                match value:
                    case ".":
                        self._grid[y][x] = Material.PATH
                    case "#":
                        self._grid[y][x] = Material.WALL

    def top_left(self) -> Coord:
        for x, material in enumerate(self._grid[0]):
            if material == Material.PATH:
                return Coord(x, 0)

    def get(self, coord: Coord) -> Material | None:
        if not self.in_bounds(coord):
            return None
        return self._grid[coord.y][coord.x]

    def in_bounds(self, coord: Coord) -> bool:
        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    def get_next(self, position: Coord, direction: Orientation) -> Coord | None:
        if not self.in_bounds(position):
            return None
        next_position = position.move(direction)
        while not self.in_bounds(next_position) or self.get(next_position) == Material.VOID:
            if not self.in_bounds(next_position):
                match (next_position.x, next_position.y):
                    case (x, -1):
                        next_position = Coord(x, self.height - 1)
                    case (x, self.height):
                        next_position = Coord(x, 0)
                    case (-1, y):
                        next_position = Coord(self.width - 1, y)
                    case (self.width, y):
                        next_position = Coord(0, y)
            else:
                next_position = next_position.move(direction)
        if self.get(next_position) == Material.WALL:
            return None
        return next_position

    def stringify(self) -> str:
        out = ""
        for row in self._grid:
            for material in row:
                match material:
                    case Material.VOID:
                        out += " "
                    case Material.PATH:
                        out += "."
                    case Material.WALL:
                        out += "#"
            out += "\n"
        return out


class CubeFace:
    top_left: Coord
    neighbors: dict[Orientation, CubeFace]
    _grid: list[list[Material]]
    _grove_map: Map

    def __init__(self, x_offset: int, y_offset: int, dimension: int, grove_map: Map) -> None:
        self.top_left = Coord(x_offset, y_offset)
        self._grove_map = grove_map
        self._grid = [[Material.PATH for _ in range(dimension)] for _ in range(dimension)]
        for y in range(dimension + y_offset, y_offset):
            for x in range(dimension + x_offset, x_offset):
                if grove_map.get(Coord(x, y)) == Material.WALL:
                    self._grid[y][x] = Material.WALL

        self.neighbors = {}

    def add_neighbor(self, face: CubeFace, direction: Orientation) -> None:
        if direction in self.neighbors:
            return
        self.neighbors[direction] = face
        face.add_neighbor(self, direction.turn(Turn.LEFT).turn(Turn.LEFT))


class CubeMap:
    top: CubeFace
    bottom: CubeFace
    left: CubeFace
    right: CubeFace
    front: CubeFace
    back: CubeFace
    _grove_map: Map

    def __init__(self, lines: list[str], dimension: int) -> None:
        self._grove_map = Map(lines)
        top_left = self._grove_map.top_left()
        moves = [
            (Orientation.RIGHT, Coord(dimension, 0)),
            (Orientation.LEFT, Coord(-dimension, 0)),
            (Orientation.DOWN, Coord(0, dimension)),
            (Orientation.UP, Coord(0, -dimension)),
        ]

        face = CubeFace(top_left.x, top_left.y, dimension, self._grove_map)
        faces = {face}
        queue = [face]
        for direction, move in moves:
            face = queue.pop()
            if face in faces:
                continue
            faces.add(face)
            position = face.top_left + move
            if self._grove_map.get(position) != Material.VOID:
                neighbor = CubeFace(top_left.x - dimension, top_left.y, dimension, self._grove_map)
                face.add_neighbor(neighbor, Orientation.LEFT)
                queue.append(neighbor)

@dataclass
class Player:
    position: Coord
    orientation: Orientation
    history: list[tuple[Coord, Orientation]] = field(init=False)

    def __post_init__(self) -> None:
        self.history = [(self.position, self.orientation)]

    def __str__(self) -> str:
        return f"{self.position} - {self.orientation.value}"

    def turn(self, turn: Turn) -> None:
        self.orientation = self.orientation.turn(turn)

    def move(self, distance: int, grove_map: Map) -> None:
        position = self.position
        for _ in range(distance):
            next_position = grove_map.get_next(position, self.orientation)
            if not next_position:
                break
            position = next_position
        self.position = position
        self.history.append((self.position, self.orientation))

    def score(self) -> int:
        return (self.position.y + 1) * 1000 + (self.position.x + 1) * 4 + self.orientation.points()


def parse_moves(moves: str) -> list[int | Turn]:
    distances = [int(distance) for distance in re.findall(r"\d+", moves)]
    turns = [Turn.LEFT if char == "L" else Turn.RIGHT for char in re.findall(r"[LR]{1}", moves)]
    out = []
    for distance, turn in zip_longest(distances, turns):
        if distance is not None:
            out.append(distance)
        if turn:
            out.append(turn)
    return out


def traverse(player: Player, grove_map: Map, moves: list[int | Turn]) -> None:
    for move in moves:
        if isinstance(move, int):
            player.move(move, grove_map)
        if isinstance(move, Turn):
            player.turn(move)


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    grove_map = Map(lines[:-2])
    moves = parse_moves(lines[-1])
    player = Player(position=grove_map.top_left(), orientation=Orientation.RIGHT)
    traverse(player, grove_map, moves)
    print(player.score())
    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
