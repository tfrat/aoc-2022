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
        if self.value is None:
            self.value = self.operation(self.left.yell(), self.right.yell())

        return self.value


class Function:
    root: Monkey
    human: Monkey
    monkeys: dict[str, Monkey]

    def __init__(self, lines: list[str]) -> None:
        self.monkeys = parse_monkeys(lines)
        self.root = self.monkeys["root"]
        self.human = self.monkeys["humn"]

    def reset(self) -> None:
        for monkey in self.monkeys.values():
            if monkey.operation:
                monkey.value = None

    def lt(self, value: int) -> bool:
        self.human.value = value
        return self.root.left.yell() < self.root.right.yell()

    def equal(self, value: int) -> bool:
        self.human.value = value
        return self.root.left.yell() == self.root.right.yell()

    def __str__(self) -> str:
        return f"{self.root.left.value} == {self.root.right.value}"


def parse_monkeys(lines: list[str]) -> dict[str, Monkey]:
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

    return monkeys


def find_human_number(lines: list[str]) -> int:
    fun = Function(lines)
    test_value = fun.human.value
    prev_value = None
    offset = 100000000
    while not fun.equal(test_value):
        difference = abs(fun.root.left.yell() - fun.root.right.yell())
        if prev_value is not None:
            if prev_value < difference:
                offset *= -1
                offset = offset // 10

        prev_value = difference
        fun.reset()
        test_value = test_value + offset
    return test_value


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    print(f"File: {filename}")
    root = parse_monkeys(lines)["root"]
    print(f"Part 1: {root.yell()}")
    print(f"Part 2: {find_human_number(lines)}")
    print()

    # solution here

    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
