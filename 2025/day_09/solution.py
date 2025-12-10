#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

import heapq
from itertools import combinations


def part1(data):
    points = parse(data)

    max = 0
    for p1, p2 in combinations(points, 2):
        a = area(p1, p2)
        if a > max:
            max = a
    answer = max
    print(f"\nPart 1: {answer}")


def part2(data):
    points = parse(data)

    hq = []
    for p1, p2 in combinations(points, 2):
        a = area(p1, p2)
        heapq.heappush(hq, (-a, (p1, p2)))

    # TODO: Compute vertical and horizontal segments. Then use those to check for invalid rectangles
    h_lines = []
    v_lines = []

    def is_valid(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        intercepts = []
        for p in points:
            x, y = p
            if p == p1 or p == p2:
                continue

            if min(x1, x2) < x < max(x1, x2):
                if min(y1, y2) < y < max(y1, y2):
                    return False

            # TODO: Replace with h/v line intercepts
            if x == x1 or x == x2:
                if min(y1, y2) < y < max(y1, y2):
                    intercepts.append((x, y))
            elif y == y1 or y == y2:
                if min(x1, x2) < x < max(x1, x2):
                    intercepts.append((x, y))
            
        xi = [x for x, y in intercepts]
        yi = [y for x, y in intercepts]

        print(xi)
        print(yi)
        if len(xi) > len(set(xi)):
            return False
        elif len(yi) > len(set(yi)):
            return False

        return True

    answer = 0
    while hq:
        a, (p1, p2) = heapq.heappop(hq)
        a = abs(a)
        #print(f"{a} - {p1} - {p2}")

        if is_valid(p1, p2):
            answer = a
            break
    print(f"\nPart 2: {answer}")


def area(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    h = abs(x2 - x1) + 1
    w = abs(y2 - y1) + 1
    return (h*w)

def parse(data):
    points = set()
    for l in data:
        x, y = [int(n) for n in l.split(",")]
        points.add((x, y))
    return points


def print_grid(red):
    xs = [x for x, _ in red]
    ys = [y for _, y in red]
    for y in range(max(ys) + 1):
        row = ""
        for x in range(max(xs) + 1):
            if (x, y) in red:
                row +="#"
            else:
                row += "."
        print(row)


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
