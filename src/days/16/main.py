from __future__ import annotations

import time
from dataclasses import dataclass


class Valve:
    name: str
    rate: int
    neighbors: set[Valve]

    def __init__(self, name: str, rate: int) -> None:
        self.name = name
        self.rate = rate
        self.neighbors = set()

    def add_neighbor(self, valve: Valve) -> None:
        self.neighbors.add(valve)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Valve) -> bool:
        return self.name == other.name


def parse_valves(lines: list[str]) -> Valve:
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
        if not start:
            start = valves[name]
        print(name, rate, neighbor_names)

    for name, valve in valves.items():
        for neighbor in valve_neighbors[name]:
            valve.add_neighbor(valves[neighbor])

    return start


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    start = parse_valves(lines)
    print(start)
    # solution here

    print()


if __name__ == '__main__':
    start_time = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start_time}")
