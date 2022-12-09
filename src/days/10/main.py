from __future__ import annotations

import time


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        moves_ = [line.rstrip() for line in f.readlines()]
    start = time.time()
    print(f"Time to execute: {time.time() - start}")
