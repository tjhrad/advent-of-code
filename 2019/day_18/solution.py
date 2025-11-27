#!/usr/bin/env python3

import helpers
from collections import defaultdict, deque
import heapq


def part1(data):
    grid = get_grid(data)
    start, keys = get_start_and_keys(grid)
    reachable_from = {}
    reachable_from['@'] = bfs_from(start, grid)
    for key in keys.keys():
        reachable_from[key] = bfs_from(keys[key], grid)
    answer = dijkstra_shortest_path(reachable_from)
    print(f"\nPart 1: {answer}")


def part2(data):
    grid = get_grid(data)
    start, keys = get_start_and_keys(grid)

    sx, sy = start
    grid[sy][sx] = "#"
    grid[sy-1][sx] = "#"
    grid[sy+1][sx] = "#"
    grid[sy][sx-1] = "#"
    grid[sy][sx+1] = "#"

    starts = [
        (sx+1, sy+1),
        (sx-1, sy+1),
        (sx+1, sy-1),
        (sx-1, sy-1),
    ]

    robots = ['@', '$', '%', '!']
    for (x, y), r in zip(starts, robots):
        grid[y][x] = r

    reachable_from = {}
    for rpos, rname in zip(starts, robots):
        reachable_from[rname] = bfs_from(rpos, grid)

    for key, pos in keys.items():
        reachable_from[key] = bfs_from(pos, grid)

    answer = dijkstra_part2(reachable_from, starts)
    print(f"\nPart 2: {answer}")


def bfs_from(pos, grid):
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    q = deque([(pos, 0, 0)]) # ((x,y), distance, requirements_mask)
    seen = {pos}
    results = {} # key -> (dist, requirement_mask)

    while q:
        (x, y), dist, req = q.popleft()
        ch = grid[y][x]

        if 'A' <= ch <= 'Z':
            req |= 1 << (ord(ch.lower()) - ord('a'))

        if 'a' <= ch <= 'z':
            results[ch] = (dist, req)

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and grid[ny][nx] != "#":
                seen.add((nx, ny))
                q.append(((nx, ny), dist + 1, req))

    return results


def dijkstra_part2(reachable_from, starts):
    ALL_KEYS = 0
    for k in reachable_from.keys():
        if k == '@':
            continue

        if 'a' <= k <= 'z':
            ALL_KEYS |= 1 << (ord(k) - ord('a'))

    robot_labels = ['@', '$', '%', '!']
    start_positions = tuple(robot_labels)

    pq = [(0, start_positions, 0)]
    best = {}

    while pq:
        dist, positions, mask = heapq.heappop(pq)

        if mask == ALL_KEYS:
            return dist

        if best.get((positions, mask), float('inf')) <= dist:
            continue
        best[(positions, mask)] = dist

        for i in range(4):
            cur = positions[i]

            for key, (d, req) in reachable_from[cur].items():

                bit = 1 << (ord(key) - ord('a'))

                if mask & bit:
                    continue

                if req & ~mask:
                    continue

                new_positions = list(positions)
                new_positions[i] = key
                new_positions = tuple(new_positions)

                newmask = mask | bit

                heapq.heappush(pq, (dist + d, new_positions, newmask))

    return None


def dijkstra_shortest_path(reachable_from):
    ALL_KEYS = 0
    for k in reachable_from.keys():
        if k == '@':
            continue

        if 'a' <= k <= 'z':
            ALL_KEYS |= 1 << (ord(k) - ord('a'))
    
    pq = [(0, "@", 0)] # dist, current_key, keys_mask
    best = {}

    while pq:
        dist, cur, mask = heapq.heappop(pq)

        if mask == ALL_KEYS:
            return dist

        if (cur, mask) in best and best[(cur, mask)] <= dist:
            continue

        best[(cur, mask)] = dist

        for key, (d, req) in reachable_from[cur].items():
            bit = 1 << (ord(key) - ord('a'))

            if mask & bit:
                continue

            if req & ~mask:
                continue

            newmask = mask | bit
            heapq.heappush(pq, (dist + d, key, newmask))

    return None


def print_grid(grid):
    for r in grid:
        print(''.join(r))


def get_grid(data):
    grid = []
    for line in data:
        grid.append([x for x in line])
    return grid


def get_start_and_keys(grid):
    keys = {}
    start = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '@':
                start = (x,y)
            if 'a' <= ch <= 'z':
                keys[ch] = (x,y)
    return start, keys


with open("./input.txt", "r") as f:
    data = [line.rstrip('\n') for line in f]


helpers.time_it(part1, data)
helpers.time_it(part2, data)
