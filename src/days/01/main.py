import heapq
with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

sum = 0
sums = []
for line in lines:
    if line == "\n":
        sums += [sum]
        sum = 0
        continue
    sum += -int(line[:-1])
if sum != 0:
    sums += [sum]

heapq.heapify(sums)
top_n = 3
max = 0
for _ in range(top_n):
    sum = heapq.heappop(sums)
    max += sum

print(f"max: {abs(max)}")
