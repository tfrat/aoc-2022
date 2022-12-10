from __future__ import annotations

import time


def render_image(raster: list[bool]) -> str:
    output = ""
    for y in range(6):
        for x in range(40):
            output += "#" if raster[(y * 40) + x] else "."
        output += "\n"
    return output


def process_image(commands: list[str]) -> list[bool]:
    raster = [False for _ in range(240)]
    register = 1
    cycle = 0
    for command in commands:
        if cycle % 40 in {register - 1, register, register + 1}:
            raster[cycle] = True
        match command.split():
            case ["addx", value]:
                cycle += 1
                if cycle % 40 in {register - 1, register, register + 1}:
                    raster[cycle] = True
                register += int(value)
            case ["noop"]:
                pass
            case _:
                pass

        cycle += 1
    return raster


def calculate_signal_strength(commands: list[str]) -> int:
    register = 1
    cycle = 1
    signal_strength = 0
    cycles = {20, 60, 100, 140, 180, 220}
    for command in commands:
        if cycle in cycles:
            signal_strength += cycle * register
        match command.split():
            case ["addx", value]:
                cycle += 1
                if cycle in cycles:
                    signal_strength += cycle * register
                register += int(value)
            case ["noop"]:
                pass
            case _:
                pass

        cycle += 1

    return signal_strength


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        commands_ = [line.rstrip() for line in f.readlines()]
    signal_strength_ = calculate_signal_strength(commands_)
    print(f"Signal Strength: {signal_strength_}")
    raster_ = process_image(commands_)
    print(render_image(raster_))
    start = time.time()
    print(f"Time to execute: {time.time() - start}")
