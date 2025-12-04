#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

import itertools


def part1(data):
    answer = max_joltage(data, 2)
    print(f"\nPart 1: {answer}")


def part2(data):
    for l in data:
        answer = max_joltage(data, 12)
    print(f"\nPart 2: {answer}")


def max_joltage(data, n):
    joltage = 0
    for line in data:
        digits = []
        i = 0
        for end in range(len(line) - n + 1, len(line) + 1):
            i += line[i:].index(max(line[i:end])) + 1
            digits.append(line[i - 1])
        joltage += int(''.join(digits))
    return joltage


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
