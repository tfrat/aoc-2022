from __future__ import annotations

import time
from dataclasses import dataclass
from typing import NewType

Minutes = NewType("Minutes", int)

class Valve:
    name: str
    rate: int
    activated: bool
    neighbors: set[Valve]

    def __init__(self, name: str, rate: int) -> None:
        self.name = name
        self.rate = rate
        self.activated = False
        self.neighbors = set()

    def add_neighbor(self, valve: Valve) -> None:
        self.neighbors.add(valve)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Valve) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        return self.activated


def parse_valves(lines: list[str]) -> tuple[Valve, set[Valve]]:
    valves = {}
    valve_neighbors = {}
    start = None
    for line in lines:
        name = line[6:8]
        rate = int(line[23:line.find(";")])
        neighbor_index = line.find("valve")

        neighbor_index = neighbor_index + 7 if line[neighbor_index+5] == "s" else neighbor_index + 6
        neighbor_names = line[neighbor_index:].split(", ")
        valves[name] = Valve(name, rate)
        valve_neighbors[name] = neighbor_names
        if start is None:
            start = valves[name]

    for name, valve in valves.items():
        for neighbor in valve_neighbors[name]:
            valve.add_neighbor(valves[neighbor])

    return start, set(valves.values())


def calculate_optimal_pressure_release(current: Valve, time_limit: Minutes, valves: set[Valve], activated: set[Valve]) -> int:
    if time_limit <= 1:
        return 0
    if valves == activated:
        return 0
    possible_release_values = []
    if current.rate == 0 and current not in activated:
        activated.add(current)
    for neighbor in current.neighbors:
        if current not in activated:
            new_activated = {current}
            new_activated.update(activated)
            value = (time_limit - 1) * current.rate + calculate_optimal_pressure_release(neighbor, Minutes(time_limit - 2), valves, new_activated)
            possible_release_values.append(value)

        value = calculate_optimal_pressure_release(neighbor, Minutes(time_limit - 1), valves, activated)
        possible_release_values.append(value)
    if possible_release_values:
        return max(possible_release_values)
    return 0


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    start, valves = parse_valves(lines)
    print(calculate_optimal_pressure_release(start, Minutes(30), valves, set()))
    # solution here

    print()


if __name__ == '__main__':
    start_time = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start_time}")
