#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    nums, symbols = parse(data)
    answer = solve(nums, symbols)
    print(f"\nPart 1: {answer}")


def part2(data):
    nums, symbols = parse2(data)
    answer = solve(nums, symbols)
    print(f"\nPart 2: {answer}")


def solve(nums, symbols):
    result = 0
    for i in range(len(nums)):
        expr = ""
        for n in nums[i]:
            expr += n + symbols[i]
        expr = expr[:-1]
        result += eval(expr)
    return result


def parse(data):
    nums = []
    symbols = []
    for line in data:
        for i, n in enumerate(line.split()):
            if n.isdigit():
                if len(nums) > i:
                    nums[i].append(n)
                else:
                    nums.append(list([n]))
            else:
                symbols.append(n)
    return nums, symbols


def parse2(data):
    nums = []
    symbols = []
    sublist = []
    for i in reversed(range(len(data[0]))):
        n = ""
        for j in range(len(data) - 1):
            if data[j][i].isdigit():
                n += data[j][i]
        if n.isdigit():
            sublist.append(n)

        if " " == data[-1][i]:
            continue
        else:
            symbols.append(data[-1][i])
            nums.append(sublist)
            sublist = list()
    return nums, symbols


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
