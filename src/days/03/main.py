def item_to_priority(item: str) -> int:
    ascii_value = ord(item)
    priority_ = 0
    if ord("A") <= ascii_value <= ord("Z"):
        priority_ += 26
    priority_ += ord(item.lower()) - ord("a") + 1
    return priority_


def split_bag(bag: str) -> tuple[str, str]:
    half_len_bag = int(len(bag)/2)
    return bag[:half_len_bag], bag[half_len_bag:]


def find_common_item(*lists: str) -> str:
    base = set(lists[0])
    for list_ in lists[1:]:
        base = base.intersection(list_)
    return next(iter(base))


def find_total_priority(bags: list[str]) -> int:
    total_priority = 0
    for bag_ in bags:
        compartment_one_, compartment_two_ = split_bag(bag_)
        common = find_common_item(compartment_one_, compartment_two_)
        priority = item_to_priority(common)
        total_priority += priority
    return total_priority


def badge_group_total_priority(bags: list[str], group_size: int) -> int:
    total = 0
    for i in range(int(len(bags) / group_size)):
        start = i * group_size
        item = find_common_item(*bags[start:start+group_size])
        total += item_to_priority(item)
    return total


if __name__ == '__main__':
    with open("input.txt", "r",
              encoding="utf-8") as f:
        bags_ = [line.strip() for line in f.readlines()]
    print("Bag Total Priority")
    print(find_total_priority(bags_))

    print("Badge Group Total Priority")
    print(badge_group_total_priority(bags_, 3))
