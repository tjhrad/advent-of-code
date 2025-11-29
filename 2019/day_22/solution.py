#!/usr/bin/env python3

import helpers


def part1(data):
    # I lost all of my work after completing this puzzle. :(
    answer = 0
    print(f"\nPart 1: {answer}")


def part2(data):
    answer = 0
    print(f"\nPart 2: {answer}")


with open("./input.txt", "r") as f:
    data = [line.rstrip('\n') for line in f]


helpers.time_it(part1, data)
helpers.time_it(part2, data)
