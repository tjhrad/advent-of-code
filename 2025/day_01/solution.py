#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(raw_input):
    pointer = 50
    answer = 0
    for seq in raw_input:
        if seq[0] == 'L':
            pointer = (pointer - int(seq[1:])) % 100
        elif seq[0] == 'R':
            pointer = (pointer + int(seq[1:])) % 100
        if pointer == 0:
            answer += 1
    print(f"\nPart 1: {answer}")


def part2(raw_input):
    pointer = 50
    answer = 0
    for seq in raw_input:
        if seq[0] == 'L':
            for _ in range(int(seq[1:])):
                pointer = (pointer - 1) % 100
                if pointer == 0:
                    answer += 1
        elif seq[0] == 'R':
            for _ in range(int(seq[1:])):
                pointer = (pointer + 1) % 100
                if pointer == 0:
                    answer += 1
    print(f"\nPart 2: {answer}")


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
