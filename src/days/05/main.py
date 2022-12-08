
def parse_crates(lines: list[str]) -> list[list[str]]:
    num_queues = int(lines[-1].strip()[-1])
    queues = [[] for _ in range(num_queues)]
    for crate_line in lines[:-1]:
        for i in range(num_queues):
            index = 1 + (4 * i)
            if index < len(crate_line):
                crate = crate_line[index].strip()
                if crate:
                    queues[i].insert(0, crate)

    return queues


def parse_move(move: str) -> tuple[int, int, int]:
    source_crate = int(move[move.index("from") + 5:move.index("to") - 1]) - 1
    target_crate = int(move[move.index("to") + 3:]) - 1
    quantity = int(move[move.index("move") + 5:move.index("from") - 1])
    return source_crate, target_crate, quantity


def execute_move_9000(queues: list[list[str]], move: str) -> list[list[str]]:
    source_crate, target_crate, quantity = parse_move(move)
    for _ in range(quantity):
        queues[target_crate].append(queues[source_crate].pop())
    return queues


def execute_move_9001(queues: list[list[str]], move: str) -> list[list[str]]:
    source_crate, target_crate, quantity = parse_move(move)
    temp = []
    for _ in range(quantity):
        temp = [queues[source_crate].pop()] + temp
    for crate in temp:
        queues[target_crate].append(crate)
    return queues


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        l = f.readline()[:-1]
        data = []
        while l:
            data += [l]
            l = f.readline()[:-1]

        crates = parse_crates(data)
        moves = [move.strip() for move in f.readlines()]

    for move in moves:
        crates = execute_move_9001(crates, move)

    print([crate[-1] for crate in crates])
