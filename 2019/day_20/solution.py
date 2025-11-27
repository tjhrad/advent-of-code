#!/usr/bin/env python3

import helpers
from collections import deque


def part1(data):
    graph, portals = parse(data)
    start = tuple(list(portals['AA'])[0])
    end = tuple(list(portals['ZZ'])[0])
    answer = bfs(graph, start, end)
    print(f"\nPart 1: {answer}")


def part2(data):
    graph, portals = parse(data)
    start = tuple(list(portals['AA'])[0])
    end = tuple(list(portals['ZZ'])[0])
    answer = bfs_part2(graph, portals, start, end)
    print(f"\nPart 2: {answer}")


def bfs(graph, start, end):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    q = deque([(start, 0)])
    seen = set()

    while q:
        current, dist = q.popleft()
        x, y = current

        if (x, y) == end:
            return dist

        for n in graph[(x, y)]:
            if n in seen:
                continue
            seen.add(n)
            q.append((n, dist + 1))


def bfs_part2(graph, portals, start, end):
    all_walkable = []
    for val in graph.values():
        [all_walkable.append(p) for p in list(val)]

    xmin = min(x for x, _ in all_walkable)
    xmax = max(x for x, _ in all_walkable)
    ymin = min(y for _, y in all_walkable)
    ymax = max(y for _, y in all_walkable)

    # state: (position, distance, layer)
    q = deque([(start, 0, 0)])
    seen = set()
    seen.add((start, 0))
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while q:
        (x, y), dist, layer = q.popleft()

        if (x, y) == end and layer == 0:
            return dist

        for nx, ny in graph[(x, y)]:
            is_teleport = abs(x - nx) + abs(y - ny) > 1

            new_layer = layer

            if is_teleport:
                is_outer = (x == xmin or x == xmax or y == ymin or y == ymax)

                if is_outer:
                    new_layer -= 1
                else:
                    new_layer += 1

                if new_layer < 0:
                    continue

            s = ((nx, ny), new_layer)
            if s in seen:
                continue

            seen.add(s)
            q.append(((nx, ny), dist + 1, new_layer))

    return None


def parse(data):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    graph = {}
    portals = {}

    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] != ".":
                continue

            neighbors = set()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if data[ny][nx] == ".":
                    neighbors.add((nx, ny))
                elif data[ny][nx].isalpha():
                    key = ""
                    if dx == 1:
                        key += data[ny][nx]
                        key += data[ny][nx + dx]
                    elif dx == -1:
                        key += data[ny][nx + dx]
                        key += data[ny][nx]
                    elif dy == -1:
                        key += data[ny + dy][nx]
                        key += data[ny][nx]
                    elif dy == 1:
                        key += data[ny][nx]
                        key += data[ny + dy][nx]
                    
                    if key in portals:
                        portals[key].add((x, y))
                    else:
                        portals[key] = set()
                        portals[key].add((x, y))

            graph[(x, y)] = neighbors
    
    for key, item in portals.items():
        if len(item) > 1:
            graph[list(item)[0]].add(list(item)[1])
            graph[list(item)[1]].add(list(item)[0])

    return graph, portals


def print_grid(grid):
    for r in grid:
        print(''.join(r))


def get_grid(data):
    grid = []
    for line in data:
        grid.append([x for x in line])
    return grid


with open("./input.txt", "r") as f:
    data = [line.rstrip('\n') for line in f]


helpers.time_it(part1, data)
helpers.time_it(part2, data)
