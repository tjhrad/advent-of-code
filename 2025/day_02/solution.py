#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(raw_input):
    ids = []
    for s in raw_input[0].split(","):
        min, max = [int(n) for n in s.split("-")]
        [ids.append(n) for n in range(min, max + 1) if not valid_id(n)]
    answer = sum(ids)
    print(f"\nPart 1: {answer}")


def part2(raw_input):
    ids = []
    for s in raw_input[0].split(","):
        min, max = [int(n) for n in s.split("-")]
        [ids.append(n) for n in range(min, max + 1) if not valid_id2(n)]
    answer = sum(ids)
    print(f"\nPart 2: {answer}")


def valid_id(n):
    nums = [x for x in str(n)]
    half = len(nums) // 2
    if nums[:half] == nums[half:]:
        return False

    return True


def valid_id2(n):
    nums = [x for x in str(n)]
    half = len(nums) // 2
    if nums[:half] == nums[half:]:
        return False

    for size in range(1, half + 1):
        chunks = [nums[i:i+size] for i in range(0, len(nums), size)]
        if chunks.count(chunks[0]) == len(chunks):
            return False

    return True
  

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
