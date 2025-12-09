#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

from itertools import combinations
import math

def part1(data):
    points = parse(data)

    dist_pairs = []
    seen = set()
    for p1, p2 in combinations(points, 2):
        if (p1, p2) in seen or (p2, p1) in seen:
            continue

        seen.add((p1, p2))
        dist = distance(p1, p2)
        dist_pairs.append((dist, p1, p2))

    sorted_pairs = sorted(dist_pairs)
    circuits = find_circuits(sorted_pairs)

    lengths = []
    for c in circuits:
        lengths.append(len(c))

    lengths.sort()
    answer = math.prod(l for l in lengths[-3:])
    print(f"\nPart 1: {answer}")


def part2(data):
    points = parse(data)

    dist_pairs = []
    seen = set()
    for p1, p2 in combinations(points, 2):
        if (p1, p2) in seen or (p2, p1) in seen:
            continue

        seen.add((p1, p2))
        dist = distance(p1, p2)
        dist_pairs.append((dist, p1, p2))

    sorted_pairs = sorted(dist_pairs)
    answer = join_all(sorted_pairs)
    print(f"\nPart 2: {answer}")


def find_circuits(sorted_pairs):
    circuits = []
    for _, p1, p2 in sorted_pairs[:1000]:
        existing_sets = []

        for s in circuits:
            if p1 in s or p2 in s:
                existing_sets.append(s)
            #if p1 in s and p2 in s:
            #    n_connections -= 1

        if not existing_sets:
            circuits.append({p1, p2})
        elif len(existing_sets) == 1:
            existing_sets[0].add(p1)
            existing_sets[0].add(p2)
        else:
            s1 = existing_sets[0]
            s2 = existing_sets[1]
            s1.update(s2)
            circuits.remove(s2)

    return [list(c) for c in circuits]


def join_all(sorted_pairs):
    circuits = []
    for _, p1, p2 in sorted_pairs:
        existing_sets = []

        for s in circuits:
            if p1 in s or p2 in s:
                existing_sets.append(s)

        if not existing_sets:
            circuits.append({p1, p2})
        elif len(existing_sets) == 1:
            existing_sets[0].add(p1)
            existing_sets[0].add(p2)
        else:
            s1 = existing_sets[0]
            s2 = existing_sets[1]
            s1.update(s2)
            circuits.remove(s2)

        if len(circuits) == 1 and len(circuits[0]) == 1000:
            return (p1[0] * p2[0])
    return None


def distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def parse(data):
    points = []
    for line in data:
        x, y, z = [int(n) for n in line.split(",")]
        points.append((x, y, z))
    return points


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
