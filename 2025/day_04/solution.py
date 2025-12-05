#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    rolls = get_rolls(data)
    answer = count_accessible_rolls(rolls)
    print(f"\nPart 1: {answer}")


def part2(data):
    rolls = get_rolls(data)
    answer = remove_rolls(rolls)
    print(f"\nPart 2: {answer}")


def get_rolls(data):
    rolls = set()
    y = 0
    for line in data:
        x = 0
        for ch in line:
            if ch == '@':
                rolls.add((x, y))
            x += 1
        y += 1
    return rolls


def remove_rolls(rolls):
    count = 0
    last_count = count
    while True:
        next_rolls = set()
        for (x, y) in rolls:
            if accessible(x, y, rolls):
                count += 1
            else:
                next_rolls.add((x, y))
        rolls = next_rolls
        if count == last_count:
            return count
        last_count = count


def count_accessible_rolls(rolls):
    count = 0
    for (x, y) in rolls:
        if accessible(x, y, rolls):
            count += 1
    return count


def accessible(x, y, rolls):
    n_adjacent = 0
    for dx, dy in [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x-1, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1)]:
        if (dx, dy) in rolls:
            n_adjacent += 1
    if n_adjacent < 4:
        return True
    return False


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
