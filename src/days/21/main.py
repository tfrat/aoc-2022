from __future__ import annotations

import operator
import re
import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    name: str
    value: int | None = None
    operation: Callable[[int, int], int] | None = None
    left: Monkey | None = None
    right: Monkey | None = None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def yell(self) -> int:
        if not self.value:
            self.value = self.operation(self.left.yell(), self.right.yell())

        return self.value


def parse_monkeys_part_one(lines: list[str]) -> Monkey:
    monkeys = {}
    monkey_friends = {}
    for line in lines:
        name = line[:4]
        if values := re.findall(r"\d+", line):
            monkeys[name] = Monkey(name, value=int(values[0]))
        else:
            left, op, right = line[5:].split()
            match op:
                case "*":
                    operation = operator.mul
                case "/":
                    operation = operator.floordiv
                case "+":
                    operation = operator.add
                case "-":
                    operation = operator.sub
                case _:
                    raise ValueError("Unsupported operator")
            monkeys[name] = Monkey(name, operation=operation)
            monkey_friends[name] = (left, right)

    for monkey, friends in monkey_friends.items():
        left, right = friends
        monkeys[monkey].left = monkeys[left]
        monkeys[monkey].right = monkeys[right]

    return monkeys["root"]



def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    root = parse_monkeys_part_one(lines)
    print(f"File: {filename}")
    print(root.yell())
    print()

    # solution here

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
