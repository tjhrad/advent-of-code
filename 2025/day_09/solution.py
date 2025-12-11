#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

import heapq
from itertools import combinations
from shapely import box, Polygon


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
    poly = Polygon(points)

    def is_rect_in_polygon(p1, p2):
        rect = box(p1[0], p1[1], p2[0], p2[1])
        return poly.contains(rect)

    hq = []
    for p1, p2 in combinations(points, 2):
        a = area(p1, p2)
        heapq.heappush(hq, (-a, (p1, p2)))

    answer = 0
    while hq:
        a, (p1, p2) = heapq.heappop(hq)

        if is_rect_in_polygon(p1, p2):
            answer = abs(a)
            break

    print(f"\nPart 2: {answer}")


def area(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    h = abs(x2 - x1) + 1
    w = abs(y2 - y1) + 1
    return (h*w)


def parse(data):
    points = []
    for l in data:
        x, y = [int(n) for n in l.split(",")]
        points.append((x, y))
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
