class Range:
    start: int
    end: int

    def __init__(self, range_str: str):
        start, end = range_str.split("-")
        self.start = int(start)
        self.end = int(end)

    def __contains__(self, item) -> bool:
        return self.start <= item.start and self.end >= item.end

    def overlaps(self, item) -> bool:
        return self.start <= item.start <= self.end


def total_contained(range_pairs: list[list[str]]) -> int:
    total = 0
    for pair in range_pairs:
        range_one = Range(pair[0])
        range_two = Range(pair[1])
        if range_two in range_one or range_one in range_two:
            total += 1
    return total


def total_overlaps(range_pairs: list[list[str]]) -> int:
    total = 0
    for pair in range_pairs:
        range_one = Range(pair[0])
        range_two = Range(pair[1])
        if range_two.overlaps(range_one) or range_one.overlaps(range_two):
            total += 1
    return total


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        pairs = [line.strip().split(",") for line in f.readlines()]

    print(total_contained(pairs))
    print(total_overlaps(pairs))
