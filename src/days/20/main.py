from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

ANSWER = [
        [1, 2, -3, 3, -2, 0, 4],
        [2, 1, -3, 3, -2, 0, 4],
        [1, -3, 2, 3, -2, 0, 4],
        [1, 2, 3, -2, -3, 0, 4],
        [1, 2, -2, -3, 0, 3, 4],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 4, 0, 3, -2]
    ]


@dataclass
class Node:
    value: int
    list_length: int
    prev: Node | None = None
    next: Node | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    def shift(self) -> None:
        left = self.value < 0
        iterations = abs(self.value) % (self.list_length + 1)
        for _ in range(iterations):
            if left:
                tmp = self.prev
                self.prev = tmp.prev
                self.next.prev = tmp
                tmp.next = self.next
                self.next = tmp
                tmp.prev = self
                self.prev.next = self
            else:
                tmp = self.next
                self.prev.next = tmp
                self.next = tmp.next
                tmp.prev = self.prev
                self.prev = tmp
                tmp.next = self
                self.next.prev = self

    def to_list(self) -> list[int]:
        out = [self.value]
        current = self.next
        while current.id != self.id:
            out += [current.value]
            current = current.next
        return out


def decrypt(code: list[int], decryption_key: int = 1, rounds: int = 1) -> int:
    decrypted = [Node(value * decryption_key, len(code)) for index, value in enumerate(code)]
    head = decrypted[0]
    prev = head
    zero_val = None
    for i in range(len(code[1:])):
        current = decrypted[i + 1]
        current.prev = prev
        current.next = decrypted[(i + 2) % len(code)]
        prev = current
        if current.value == 0:
            zero_val = current

    if not zero_val:
        raise ValueError("No zero value found")

    head.next = decrypted[1]
    head.prev = prev

    for _ in range(rounds):
        for node in decrypted:
            node.shift()

    current = zero_val
    total = 0
    for i in range(3000):
        current = current.next
        if i in {1000 - 1, 2000 - 1, 3000 - 1}:
            total += current.value
    return total


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        code = [int(line.rstrip()) for line in f.readlines()]
    print(f"File: {filename}")
    print(f"Part 1: {decrypt(code)}")
    # print(f"Part 2: {decrypt(code, 811589153, 10)}")
    print()


if __name__ == '__main__':
    start = time.time()
    # run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
