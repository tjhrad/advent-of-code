#!/usr/bin/env python3

import time
from collections import deque
import numpy as np


def time_it(func, *args, **kwargs):
    """Run a function with timing and print the elapsed time."""
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    print(format_time(elapsed))
    return result


def format_time(seconds: float) -> str:
    if seconds >= 1:
        return f"{seconds:.3f} s"
    elif seconds >= 1e-3:
        return f"{seconds * 1e3:.3f} ms"
    elif seconds >= 1e-6:
        return f"{seconds * 1e6:.3f} µs"
    else:
        return f"{seconds * 1e9:.3f} ns"


def is_integer(s):
    """
    Checks if a string is an integer
    This will ignore '+' and '-'
    """
    if s[0] in ["+", "-"]:
        if s[1:].isdigit():
            return True
        return False
      
    if s.isdigit():
        return True
    return False


def manhattan_distance(point_1, point_2):
    return sum(abs(a-b) for a, b in zip(point_1, point_2))


def topological_sort(graph):
    """
    Khan's algorithm
    graph: dict where keys are nodes, values are lists of nodes they point to
    Returns: a list of nodes in topologically sorted order
    """
    # Compute indegree of each node
    indegree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1

    # Initialize queue with nodes that have indegree 0
    queue = deque([node for node in graph if indegree[node] == 0])
    result = []

    # Process nodes
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(result) != len(graph):
        raise ValueError("Graph has a cycle! Topological sort impossible.")

    return result


def bounding_box_area(points):
    """
    Compute the bounding box of a set of points
    points = numpy array of 2d points
    size (n, 2)
    """
    xs, ys = points[:, 0], points[:, 1]
    return (xs.max() - xs.min()) * (ys.max() - ys.min())


def display_positions(starting_positions, velocities, t):
    """
    Converts a set of points to a grid and displays them.
    This can be used to display a message created by organized points on a grid
    starting_positions and velocities should both be numpy arrays of size (n, 2)
    Example: See AOC 2018 day 10
    """
    points = starting_positions + velocities * t
    xs, ys = points[:,0], points[:,1]
    xs -= xs.min()
    ys -= ys.min()
    grid = np.full((ys.max() + 1, xs.max() + 1), ' ')
    grid[ys, xs] = "#"
    print("\n".join("".join(row) for row in grid))
