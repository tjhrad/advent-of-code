#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    grid = [[1 if c != '.' else 0 for c in line] for line in data]
    seen = set()
    def save_state(grid):
        state_tuple = tuple(tuple(row) for row in grid)

        if state_tuple in seen:
            return False
        else:
            seen.add(state_tuple)
            return True

    while save_state(grid):
        grid = update_grid(grid)

    answer = biodiversity_rating(grid)
    print(f"\nPart 1: {answer}")


def part2(data):
    bugs = set()
    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            if ch == "#":
                bugs.add((0, x, y))

    for _ in range(200):
        new_bugs = set()

        candidates = set()
        for (l, x, y) in bugs:
            candidates.add((l, x, y))
            for neighbor in get_recursive_neighbors(l, x, y):
                candidates.add(neighbor)

        for (l, x, y) in candidates:
            neighbor_count = 0
            for neighbor in get_recursive_neighbors(l, x, y):
                if neighbor in bugs:
                    neighbor_count += 1

            is_bug = (l, x, y) in bugs

            if is_bug and neighbor_count == 1:
                new_bugs.add((l, x, y))
            elif not is_bug and (neighbor_count == 1 or neighbor_count == 2):
                new_bugs.add((l, x, y))

        bugs = new_bugs

    answer = len(bugs)
    print(f"\nPart 2: {answer}")


def get_recursive_neighbors(lvl, x, y):
    neighbors = []

    for nx, ny in [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]:

        if nx == 2 and ny == 2:
            if x == 1:
                neighbors.extend([(lvl + 1, 0, i) for i in range(5)])
            elif x == 3:
                neighbors.extend([(lvl + 1, 4, i) for i in range(5)])
            elif y == 1:
                neighbors.extend([(lvl + 1, i, 0) for i in range(5)])
            elif y == 3:
                neighbors.extend([(lvl + 1, i, 4) for i in range(5)])

        elif nx < 0:
            neighbors.append((lvl - 1, 1, 2))
        elif nx > 4:
            neighbors.append((lvl - 1, 3, 2))
        elif ny < 0:
            neighbors.append((lvl - 1, 2, 1))
        elif ny > 4:
            neighbors.append((lvl - 1, 2, 3))

        else:
            neighbors.append((lvl, nx, ny))

    return neighbors


def biodiversity_rating(grid):
    points = 1
    rating = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                rating += points
            points *= 2
    return rating


def update_grid(grid):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    new_grid = [[cell for cell in row] for row in grid]
    for y in range(len(new_grid)):
        for x in range(len(new_grid[0])):
            bugs = 0
            empty = 0
            for nx, ny in dirs:
                dx, dy = x+nx, y+ny
                if dx < 0 or dx >= len(new_grid[0]):
                    continue
                if dy < 0 or dy >= len(new_grid):
                    continue

                if grid[dy][dx] == 0:
                    empty += 1
                elif grid[dy][dx] == 1:
                    bugs += 1

            if grid[y][x] == 1 and bugs != 1:
                new_grid[y][x] = 0
            elif grid[y][x] == 0 and 1 <= bugs <= 2:
                new_grid[y][x] = 1

    return new_grid


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
