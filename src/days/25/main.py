from __future__ import annotations

import time
from dataclasses import dataclass, field


SNAFU_VALUES = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}


@dataclass(frozen=True)
class Snafu:
    value: str
    digits: list[int] = field(init=False)

    def __post_init__(self) -> None:
        # Set the value of a frozen dataclass
        super().__setattr__("digits", [SNAFU_VALUES[char] for char in reversed(self.value)])

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    @property
    def base_10(self) -> int:
        out = 0
        for power, digit in enumerate(self.digits):
            out += pow(5, power) * digit
        return out




def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    snafus = [Snafu(line) for line in lines]
    for snafu in snafus:
        print(f"{snafu} = {snafu.base_10}")

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    # run("input.txt")
    print(f"Time to execute: {time.time() - start}")
