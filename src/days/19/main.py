from __future__ import annotations

import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import NewType


class Material(Enum):
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"


RobotCost = NewType("RobotCost", dict[Material, int])


@dataclass
class Robots:
    cost: RobotCost
    material: Material
    robots: int = 0
    count: int = 0

    def add_robot(self) -> int:
        self.robots += 1
        return self.robots

    def collect(self) -> int:
        return self.robots


@dataclass
class MaterialSupply:
    materials: dict[Material, int] = field(default_factory=lambda: defaultdict(lambda: 0))

    def __str__(self) -> str:
        return ", ".join([f"{material.value}: {quantity}" for material, quantity in self.materials.items()])

    def add_material(self, material: Material, quantity: int) -> int:
        self.materials[material] += quantity
        return self.materials[material]

    def consume_materials(self, robot_cost: RobotCost) -> bool:
        for material, quantity in robot_cost.items():
            if self.materials[material] - quantity < 0:
                return False
        for material, quantity in robot_cost.items():
            self.materials[material] -= quantity
        return True


@dataclass
class RobotFactory:
    id: int
    costs: dict[Material, RobotCost]
    robots: list[Robots] = field(init=False)
    supply: MaterialSupply = field(default=MaterialSupply(), init=False)

    def __post_init__(self) -> None:
        self.robots = [
            Robots(self.costs[Material.GEODE], Material.GEODE),
            Robots(self.costs[Material.OBSIDIAN], Material.OBSIDIAN),
            Robots(self.costs[Material.CLAY], Material.CLAY),
            Robots(self.costs[Material.ORE], Material.ORE, robots=1),
        ]

    def __str__(self) -> str:
        return f"{self.supply}"

    def __repr__(self) -> str:
        return str(self)

    def build(self) -> None:
        for robot in self.robots:
            if self.supply.consume_materials(robot.cost):
                robot.add_robot()
            self.supply.add_material(robot.material, robot.collect())

    def get_supply(self, material: Material) -> int:
        return self.supply.materials[material]


def build_factories(lines: list[str]) -> list[RobotFactory]:
    factories = []
    for line in lines:
        numbers = re.findall(r"\d+", line)
        blueprint_id = int(numbers[0])
        ore_cost = defaultdict(lambda: 0)
        ore_cost[Material.ORE] = int(numbers[1])
        clay_cost = defaultdict(lambda: 0)
        clay_cost[Material.ORE] = int(numbers[2])
        obsidian_cost = defaultdict(lambda: 0)
        obsidian_cost[Material.ORE] = int(numbers[3])
        obsidian_cost[Material.CLAY] = int(numbers[4])
        geode_cost = defaultdict(lambda: 0)
        geode_cost[Material.ORE] = int(numbers[5])
        geode_cost[Material.OBSIDIAN] = int(numbers[6])
        costs = {
            Material.ORE: ore_cost,
            Material.CLAY: clay_cost,
            Material.OBSIDIAN: obsidian_cost,
            Material.GEODE: geode_cost
        }
        factories.append(RobotFactory(blueprint_id, costs))
    return factories


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    factories = build_factories(lines)
    minutes = 24
    for minute in range(minutes):
        for factory in factories:
            factory.build()
    total_geodes = sum([factory.supply.materials[Material.GEODE] for factory in factories])
    print(total_geodes)


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
