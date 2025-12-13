#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

from itertools import combinations


def part1(data):
    nums = [int(n) for n in data]
    answer = sum([n1*n2 for n1, n2 in combinations(nums, 2) if n1+n2 == 2020])
    print(f"\nPart 1: {answer}")


def part2(data):
    nums = [int(n) for n in data]
    answer = sum([n1*n2*n3 for n1, n2, n3 in combinations(nums, 3) if n1+n2+n3 == 2020])
    print(f"\nPart 2: {answer}")


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
