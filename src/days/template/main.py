from __future__ import annotations

import time


def run() -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]


if __name__ == '__main__':
    start = time.time()
    run()
    print(f"Time to execute: {time.time() - start}")
