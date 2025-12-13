#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    regions, quantities = parse(data)
    answer = sum([1 for i in range(len(regions)) if boxes_fit(regions[i], quantities[i])])
    print(f"\nPart 1: {answer}")


def boxes_fit(region, target):
    if (region[0] * region[1]) >= (9 * sum(target)):
        return True
    return False


def parse(data):
    regions, quantities = [], []
    for i in range(len(data)):
        if 'x' in data[i]:
            size, qs = data[i].split(": ")
            dims = tuple([int(n) for n in size.split("x")])
            quantities.append([int(n) for n in qs.split()])
            regions.append(dims)
    return regions, quantities


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


if __name__ == "__main__":
    main()
