#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

import math


def part1(data):
    grid = parse(data)
    answer = count_trees(grid, 3, 1)
    print(f"\nPart 1: {answer}")


def part2(data):
    grid = parse(data)
    answer = math.prod([count_trees(grid, dx, dy) for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]])
    print(f"\nPart 2: {answer}")
    

def parse(data):
    grid = []
    for line in data:
        grid.append([ch for ch in line])
    return grid


def count_trees(grid, dx, dy):
    count = 0
    x, y = 0, 0
    while y < len(grid):
        if grid[y][x] == '#':
            count += 1
        x = (x + dx) % len(grid[0])
        y += dy
    return count

    
def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    try:
        data = read_input(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
        return

    start_time = time.time()
    part1(data)
    print(format_time(time.time() - start_time))

    start_time = time.time()
    part2(data)
    print(format_time(time.time() - start_time))


if __name__ == "__main__":
    main()
