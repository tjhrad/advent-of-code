#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

from functools import cache
from collections import defaultdict


def part1(data):
    graph = parse(data)

    @cache
    def count_paths(current):
        count = 0

        if current == 'out':
            return 1

        for n in graph[current]:
            count += count_paths(n)

        return count

    answer = count_paths('you')
    print(f"\nPart 1: {answer}")


def part2(data):
    graph = parse(data)

    @cache
    def count_paths(current, seen_dac, seen_fft):
        count = 0

        if current == 'out':
            if seen_dac and seen_fft:
                return 1
            else:
                return 0
        elif current == 'dac':
            seen_dac = True
        elif current == 'fft':
            seen_fft = True

        for n in graph[current]:
            count += count_paths(n, seen_dac, seen_fft)

        return count

    answer = count_paths('svr', False, False)
    print(f"\nPart 2: {answer}")


def parse(data):
    graph = defaultdict(list)
    for line in data:
        key, items = line.split(": ")
        for i in items.split():
            graph[key].append(i)
    return graph


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
