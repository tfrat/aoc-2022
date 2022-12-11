from __future__ import annotations

import math
from dataclasses import  dataclass
import time


@dataclass
class Operation:
    left_operand: str
    right_operand: str
    operation: str

    def calculate(self, old: int) -> int:
        left = old if self.left_operand == "old" else int(self.left_operand)
        right = old if self.right_operand == "old" else int(self.right_operand)
        match self.operation:
            case "*":
                return left * right
            case "-":
                return left - right
            case "+":
                return left + right
            case "/":
                return int(left / right)


@dataclass
class Monkey:
    items: list[int]
    operation: Operation
    test_value: int
    true_target: int
    false_target: int

    def catch(self, item: int) -> None:
        self.items.append(item)

    def item_pass(self, lcm: int) -> tuple[int, int] | None:
        if not self.items:
            return None
        item = self.items.pop()
        worry_level = self.operation.calculate(item)
        reduced_item = worry_level % lcm
        if worry_level % self.test_value == 0:
            return reduced_item, self.true_target
        return reduced_item, self.false_target


def gen_monkeys(lines: list[str]) -> list[Monkey]:
    monkeys = []
    for i in range(int((len(lines) + 1) / 7)):
        offset = i * 7
        starting_items = [int(item) for item in lines[offset + 1][len("  Starting items: "):].split(", ")]
        starting_items.reverse()
        operation = lines[offset + 2][len("  Operation: new = "):].split()
        test = int(lines[offset + 3][len("  Test: divisible by "):])
        true = int(lines[offset + 4][len("    If true: throw to monkey "):])
        false = int(lines[offset + 5][len("    If false: throw to monkey "):])
        monkeys.append(Monkey(starting_items, Operation(operation[0], operation[2], operation[1]), test, true, false))
    return monkeys


def calculate_monkey_business(monkeys: list[Monkey], rounds: int) -> int:
    monkey_activity = [0 for _ in range(len(monkeys))]
    lcm = math.lcm(*[monkey.test_value for monkey in monkeys])
    for i in range(rounds):
        for index, monkey in enumerate(monkeys):
            while item_pass := monkey.item_pass(lcm):
                monkey_activity[index] += 1
                item, target_monkey = item_pass
                monkeys[target_monkey].catch(item)

    monkey_activity.sort()
    return monkey_activity[-1] * monkey_activity[-2]


def run() -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    monkeys = gen_monkeys(lines)
    print(calculate_monkey_business(monkeys, 10000))


if __name__ == '__main__':
    start = time.time()
    run()
    print(f"Time to execute: {time.time() - start}")
