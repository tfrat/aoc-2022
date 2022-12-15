from __future__ import annotations

import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def taxi_distance(self, other: Coord) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Sensor:
    location: Coord
    closest_beacon: Coord
    distance: int

    def __init__(self, location: Coord, closest_beacon: Coord) -> None:
        self.location = location
        self.closest_beacon = closest_beacon
        self.distance = location.taxi_distance(closest_beacon)

    def __str__(self) -> str:
        return f"{self.location.x}, {self.location.y}"

    def get_x_range(self, y: int) -> tuple[int, int] | None:
        if self.location.y - self.distance <= y <= self.location.y + self.distance:
            offset = self.distance - abs(self.location.y - y)
            return self.location.x - offset, self.location.x + offset
        return None


def merge_intervals(intervals: list[tuple], left_limit: int, right_limit: int) -> list[tuple]:
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    current = None
    for interval in sorted_intervals:
        if current is None:
            current = interval
            continue
        if interval[0] <= current[1]:
            current = (max(current[0], left_limit), min(right_limit, max(current[1], interval[1])))
        else:
            if current[0] > right_limit:
                break
            merged.append(current)
            current = None
    if current and current[0] < right_limit:
        merged.append(current)
    return merged


def calculate_total(intervals: list[tuple[int, int]]) -> int:
    total = 0
    for interval in intervals:
        total += abs(interval[1] - interval[0]) + 1

    return total


def row_intervals(sensors: list[Sensor], y: int, left_limit: int = -sys.maxsize, right_limit: int = sys.maxsize) -> list[tuple[int,int]]:
    return merge_intervals([sensor.get_x_range(y) for sensor in sensors if sensor.get_x_range(y)], left_limit, right_limit)


def find_beacon(sensors: list[Sensor], limit: int) -> Coord:
    for y in range(limit + 1):
        intervals = row_intervals(sensors, y, 0, limit)
        if len(intervals) > 1:
            return Coord(intervals[0][1] + 1, y)
    raise ValueError("No Beacon found")


def get_sensors(lines: list[str]) -> list[Sensor]:
    sensors = []

    for line in lines:
        x = int(line[line.find("x=") + 2:line.find(", y")])
        y = int(line[line.find(", y=") + 4:line.find(": closest beacon")])
        sensor_loc = Coord(x, y)
        x = int(line[line.rfind("x=") + 2:line.rfind(", y")])
        y = int(line[line.rfind("y=") + 2:])
        sensor = Sensor(sensor_loc, Coord(x, y))
        sensors.append(sensor)

    return sensors


def run(filename: str, target_y: int, limit: int) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    sensors = get_sensors(lines)
    print(f"Lines covered at y=10: {calculate_total(row_intervals(sensors, target_y))}")

    try:
        beacon = find_beacon(sensors, limit)
        print(beacon)
        print(f"Tuning Frequency: {beacon.x * 4000000 + beacon.y}")
    except ValueError as e:
        print(e)
    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt", 10, 20)
    run("input.txt", 2000000, 4000000)
    print(f"Time to execute: {time.time() - start}")
