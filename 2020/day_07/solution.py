#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

from collections import deque
from functools import cache


def part1(data):
    bags = parse(data)
    answer = sum([1 for name in bags.keys() if bfs(bags, name, "shiny gold")])
    print(f"\nPart 1: {answer}")


def part2(data):
    bags = parse(data)
    answer = total_bags(bags)
    print(f"\nPart 2: {answer}")


def total_bags(bags):

    @cache
    def count_bags(b):
        if b not in bags:
            return 1
        
        count = 1
        
        for n, name in bags[b]:
            count += (n * count_bags(name))

        return count

    return count_bags("shiny gold") - 1


def bfs(graph, start, end):
    if start == end:
        return False
    
    q = deque([start])
    seen = set()

    while q:
        current = q.popleft()

        if current == end:
            return True

        seen.add(current)

        if current not in graph:
            continue

        for _, next_bag in graph[current]:
            if next_bag in seen:
                continue

            q.append(next_bag)
    return False


def parse(data):
    bags = dict()
    for line in data:
        if "no" in line:
            continue

        parts = line.split(" contain ")
        key = parts[0].replace(" bags", "")
        items = []
        for parts2 in parts[1].split(","):
            n, c1, c2, _ = parts2.split()
            n = int(n)
            name = c1 + " " + c2
            items.append((n, name))
        bags[key] = items
    return bags


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
