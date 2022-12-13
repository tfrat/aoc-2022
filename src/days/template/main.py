from __future__ import annotations

import time


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")

    # solution here

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
