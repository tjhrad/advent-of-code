#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    ranges, available_ids = parse(data)
    answer = sum([1 for n in available_ids if fresh(n, ranges)])
    print(f"\nPart 1: {answer}")


def part2(data):
    ranges, _ = parse(data)
    answer = count_total(ranges)
    print(f"\nPart 2: {answer}")


def count_total(ranges):
    count = 0
    for min, max in ranges:
        count += (max - min + 1)
    return count


def fresh(n, ranges):
    for min, max in ranges:
        if min <= n <= max:
            return True
    return False


def parse(data):
    ranges = []
    available_ids = []
    for line in data:
        if "-" in line:
            min, max = [int(n) for n in line.split("-")]
            ranges.append((min, max))
        elif line.isdigit():
            available_ids.append(int(line))

    ranges = fix_overlap(ranges)
    return ranges, available_ids


def fix_overlap(ranges):
    ranges = sorted(ranges)
    fixed_ranges = []

    for current in ranges:
        if not fixed_ranges:
            fixed_ranges.append(current)
            continue

        last = fixed_ranges[-1]

        if current[0] <= last[1]:
            merged = (last[0], max(last[1], current[1]))
            fixed_ranges[-1] = merged
        else:
            fixed_ranges.append(current)

    return fixed_ranges


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
