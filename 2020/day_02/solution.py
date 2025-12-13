#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    ranges, conditions, passwords = parse(data)
    answer = sum([1 for i in range(len(ranges)) if ranges[i][0] <= passwords[i].count(conditions[i]) <= ranges[i][1]])
    print(f"\nPart 1: {answer}")


def part2(data):
    ranges, conditions, passwords = parse(data)
    answer = 0
    for i in range(len(ranges)):
        cond1 = passwords[i][ranges[i][0] - 1] == conditions[i]
        cond2 = passwords[i][ranges[i][1] - 1] == conditions[i]
        if (cond1 and not cond2) or (not cond1 and cond2):
            answer += 1
    print(f"\nPart 2: {answer}")


def parse(data):
    ranges, conditions, passwords = [], [], []
    for line in data:
        r, c, p = line.split()
        ranges.append(tuple([int(n) for n in r.split('-')]))
        conditions.append(c[:-1])
        passwords.append(p)
    return ranges, conditions, passwords


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
