#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    grid, splitters, start = parse(data)
    answer = simulate(start, splitters)
    print(f"\nPart 1: {answer}")


def part2(data):
    grid, splitters, start = parse(data)
    answer = simulate_timelines(start, splitters)
    print(f"\nPart 2: {answer}")


def simulate(start, splitters):
    q = [start]
    seen = set()
    count = 0
    max_y = max([y for _, y in splitters]) + 1

    while q:
        current = q.pop(0)
        (x, y) = current

        if current in seen:
            continue

        seen.add(current)

        if (x, y + 1) in splitters:
            count += 1
            for n in [(x + 1, y), (x - 1, y)]:
                if n in splitters:
                    continue

                q.append(n)
        elif y < max_y:
            q.append((x, y + 1))

    return count


def simulate_timelines(start, splitters):
    (sx, sy) = start
    q = [(sx, sy, 1)]
    count = 0
    max_y = max([y for _, y in splitters]) + 1

    while q:
        row_blocks = {}

        for current in q:
            (x, y, t) = current

            if y >= max_y:
                count += t
                continue
           
            if (x, y + 1) in splitters:
                for n in [(x + 1, y), (x - 1, y)]:
                    if n in splitters:
                        continue

                    if n in row_blocks:
                        row_blocks[n] += t
                    else:
                        row_blocks[n] = t
            elif y < max_y:
                if (x, y + 1) in row_blocks:
                    row_blocks[(x, y + 1)] += t
                else:
                    row_blocks[(x, y + 1)] = t

        q.clear()
        for (rx, ry), rt in row_blocks.items():
            q.append((rx, ry, rt))

    return count


def parse(data):
    start = None
    splitters = []
    grid = []
    for y in range(len(data)):
        row = []
        for x in range(len(data[0])):
            row.append(data[y][x])
            if data[y][x] == 'S':
                start = (x, y)
            elif data[y][x] == '^':
                splitters.append((x, y))
        grid.append(row)
    return grid, splitters, start


def print_grid(grid):
    for row in grid:
        print(''.join(row))

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    try:
        raw_input = read_input(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
        return

    start_time = time.time()
    part1(raw_input)
    print(format_time(time.time() - start_time))

    start_time = time.time()
    part2(raw_input)
    print(format_time(time.time() - start_time))


if __name__ == "__main__":
    main()
