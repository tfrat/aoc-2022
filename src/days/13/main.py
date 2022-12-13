from __future__ import annotations

import builtins
import time


def is_correct(first_packet: list[int | str], second_packet: list[int | str]) -> tuple[bool, bool]:
    for first, second in zip(first_packet, second_packet):
        match (type(first), type(second)):
            case (builtins.int, builtins.int):
                if first < second:
                    return True, True
                if first > second:
                    return False, True
            case (builtins.list, builtins.int):
                ans, escape = is_correct(first, [second])
                if escape:
                    return ans, True
                if not ans:
                    return False, False
            case (builtins.int, builtins.list):
                ans, escape = is_correct([first], second)
                if escape:
                    return ans, True
                if not ans:
                    return False, False
            case (builtins.list, builtins.list):
                ans, escape = is_correct(first, second)
                if escape:
                    return ans, True
                if not ans:
                    return False, False

    if len(first_packet) < len(second_packet):
        return True, True
    if len(first_packet) > len(second_packet):
        return False, True
    return True, False


class Packet:
    contents: list[int | str]

    def __init__(self, contents: list[int | str]) -> None:
        self.contents = contents

    def __eq__(self, other: Packet) -> bool:
        return self.contents == other.contents

    def __cmp__(self, other: Packet) -> int:
        if self.contents == other.contents:
            return 0
        if is_correct(self.contents, other.contents)[0]:
            return -1
        return 1

    def __lt__(self, other: Packet) -> bool:
        return self.__cmp__(other) == -1

    def __str__(self) -> str:
        return str(self.contents)


def count_correct_pairs(pairs: list[tuple]) -> int:
    correct_pairs = 0
    for i, pair in enumerate(pairs):
        ans, escaped = is_correct(*pair)
        if ans:
            correct_pairs += i + 1
    return correct_pairs


def find_decoder_key(packets: list[Packet]) -> int:
    sorted_packets = sorted(packets)
    product = 1
    for i, packet in enumerate(sorted_packets):
        if packet.contents == list([2]) or packet.contents == list([6]):
            product *= (i + 1)

    return product


def run(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
        packet_pairs = []
        for i in range(0, len(lines), 3):
            packet_pairs.append((eval(lines[i]), eval(lines[i + 1])))
    print(f"File: {filename}")
    print(f"Correct pairs: {count_correct_pairs(packet_pairs)}")

    packets = [Packet(list(list([2]))), Packet(list(list([6])))]
    for pair in packet_pairs:
        packets.append(Packet(pair[0]))
        packets.append(Packet(pair[1]))

    print(f"Decoder key: {find_decoder_key(packets)}")
    print()


if __name__ == '__main__':
    start = time.time()
    run("example.txt")
    run("input.txt")
    print(f"Time to execute: {time.time() - start}")
