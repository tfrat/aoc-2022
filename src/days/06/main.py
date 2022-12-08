from collections import Counter


def find_first_marker(code: str, unique_count: int) -> int:
    counter = Counter(code[:unique_count])
    for i, c in enumerate(code[unique_count:]):
        if len(counter) == unique_count:
            return i + unique_count
        counter.update(c)
        counter[code[i]] -= 1
        if counter[code[i]] == 0:
            counter.pop(code[i])
    raise ValueError("No marker found")


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        encoding = f.readline().strip()
    print(find_first_marker(encoding, 4))
    print(find_first_marker(encoding, 14))
