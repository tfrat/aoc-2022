from __future__ import annotations

import sys
import time


def taxi_distance(first: tuple[int, int], second: tuple[int, int]) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


class Sensor:
    location: tuple[int, int]
    closest_beacon: tuple[int, int]
    distance: int

    def __init__(self, location: tuple[int, int], closest_beacon: tuple[int, int]) -> None:
        self.location = location
        self.closest_beacon = closest_beacon
        self.distance = taxi_distance(location, closest_beacon)

    def __lt__(self, other: Sensor) -> bool:
        origin = (0, 0)
        return taxi_distance(self.location, origin) < taxi_distance(other.location, origin)

    def in_range(self, coord: tuple[int, int]) -> bool:
        return taxi_distance(self.location, coord) <= self.distance


def count_no_beacons(sensors: list[Sensor], y: int, min_x: int, max_x: int) -> int:
    hits = set()
    sorted_sensors = sorted(sensors)
    for x in range(min_x, max_x):
        location = (x, y)
        if location in hits:
            continue
        for sensor in sorted_sensors:
            if sensor.in_range(location) and location != sensor.closest_beacon:
                hits.add(location)
    return len(hits)


def find_beacon(sensors: list[Sensor], top_left: tuple[int, int], bottom_right: tuple[int,int]) -> set[tuple]:
    hits = set()
    for x in range(top_left[0], bottom_right[0] + 1):
        for y in range(top_left[1], bottom_right[1] + 1):
            location = (x, y)
            if location in hits:
                continue
            hit = False
            for sensor in sensors:
                if sensor.in_range(location):
                    hit = True
                    break
            if not hit:
                hits.add(location)
    return hits


def get_sensors(lines: list[str]) -> tuple[list[Sensor], int, int]:
    sensors = []
    min_x = sys.maxsize
    max_x = -sys.maxsize

    for line in lines:
        x = int(line[line.find("x=") + 2:line.find(", y")])
        y = int(line[line.find(", y=") + 4:line.find(": closest beacon")])
        sensor_loc = (x, y)
        x = int(line[line.rfind("x=") + 2:line.rfind(", y")])
        y = int(line[line.rfind("y=") + 2:])
        sensor = Sensor(sensor_loc, (x, y))
        sensors.append(sensor)
        max_x = max(sensor.location[0] + sensor.distance, max_x)
        min_x = min(sensor.location[0] - sensor.distance, min_x)

    return sensors, min_x, max_x


def run(filename: str, y: int, part_2_bound: tuple[int, int]) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    sensors, min_x, max_x = get_sensors(lines)
    print(count_no_beacons(sensors, y, min_x, max_x))
    # beacons = find_beacon(sensors, (0, 0), part_2_bound)
    # print(beacons)
    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt", 10, (20, 20))
    run("input.txt", 2000000, (4000000, 4000000))
    print(f"Time to execute: {time.time() - start}")
