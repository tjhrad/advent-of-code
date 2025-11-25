#!/usr/bin/env python3

import helpers
from collections import defaultdict, deque


def part1(data):
    start_pos, map, keys, doors = parse_data(data)
    path = find_keys(start_pos, map, keys, doors)
    answer = len(path)
    print(f"\nPart 1: {answer}")


def part2(data):
    answer = 0
    print(f"\nPart 2: {answer}")


def find_keys(start, map, keys, doors):
    # pos, [path], [keys_collected]
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    queue = deque([[start, [], set()]])
    seen = set()

    while queue:
        current_pos, current_path, current_keys = queue.popleft()

        if len(current_keys) == len(keys):
            return current_path

        #current_str = str(current_pos) + "-" + ''.join(str(x) for x in sorted(current_keys))
        #print(current_str)
        #seen.add(current_str)

        for d in DIRECTIONS:
            next_pos = (current_pos[0] + d[0], current_pos[1] + d[1])

            next_str = str(next_pos) + "-" + ''.join(str(x) for x in sorted(current_keys))

            if next_str in seen:
                continue

            if next_pos not in map:
                continue

            if map[next_pos] == "#":
                continue

            if next_pos in doors and doors[next_pos].lower() not in current_keys:
                continue

            seen.add(next_str)

            if next_pos in map and map[next_pos] == ".":
                if next_pos in keys:
                    queue.append([next_pos, current_path + [next_pos], current_keys | set(keys[next_pos])])
                else:
                    queue.append([next_pos, current_path + [next_pos], current_keys])
    
    print("No path found.")
    return None


def print_map(map):
    xs = [x for x, _ in map.keys()]
    ys = [y for _, y in map.keys()]

    for y in range(min(ys), max(ys) + 1):
        row = ""
        for x in range(min(xs), max(xs) + 1):
            row += map[(x, y)]
        print(row)


def parse_data(data):
    x, y = 0, 0
    start_pos = None
    map = defaultdict(str)
    keys = defaultdict(str)
    doors = defaultdict(str)

    for line in data:
        for c in line:
            if c in "#.":
                map[(x, y)] = c
            elif c == "@":
                map[(x, y)] = "."
                start_pos = (x, y)
            elif c.islower():
                map[(x, y)] = "."
                keys[(x, y)] = c
            elif c.isupper():
                map[(x, y)] = "."
                doors[(x, y)] = c
            else:
                map[(x, y)] = "."

            x += 1
        y += 1
        x = 0

    return start_pos, map, keys, doors


with open("./input.txt", "r") as f:
    data = [line.rstrip('\n') for line in f]


helpers.time_it(part1, data)
helpers.time_it(part2, data)
