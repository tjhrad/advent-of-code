#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    answer = max([(find_middle(line[:7], 0, 127) * 8) + find_middle(line[-3:], 0, 7) for line in data])
    print(f"\nPart 1: {answer}")


def part2(data):
    all_ids = get_ids()
    taken_ids = [(find_middle(line[:7], 0, 127) * 8) + find_middle(line[-3:], 0, 7) for line in data]
    answer = find_seat(all_ids, taken_ids)
    print(f"\nPart 2: {answer}")


def find_seat(all_ids, taken_ids):
    for i in range(len(all_ids)):
        if all_ids[i] in taken_ids:
            continue

        if all_ids[i-1] not in taken_ids:
            continue

        if all_ids[i+1] not in taken_ids:
            continue

        return all_ids[i]
    return None


def find_middle(s, min_n, max_n):
    for ch in s:
        if ch in 'FL':
            max_n = (min_n + max_n) // 2
        elif ch in 'BR':
            min_n = (min_n + max_n) // 2
        else:
            print("Error: unknown char: {ch}")
            return None
    return max_n


def get_ids():
    ids = []
    for r in range(1, 126):
        for c in range(0, 7):
            ids.append((r*8) + c)
    return ids


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
