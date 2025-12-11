#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input

import pulp

def part1(data):
    targets, buttons, joltages = parse(data)    

    answer = 0
    for i in range(len(targets)):
        answer += start_machine(targets[i], buttons[i])
    print(f"\nPart 1: {answer}")


def part2(data):
    targets, buttons, joltages = parse(data)    
    answer = 0
    for i in range(len(targets)):
        answer += configure_joltage(joltages[i], buttons[i])
    print(f"\nPart 2: {answer}")


def start_machine(target, buttons):
    n_lights = len(target)
    starting_state = [0] * n_lights
    q = [(0, starting_state)]
    seen = set()

    while q:
        n, state = q.pop(0)

        if tuple(state) in seen:
            continue

        if state == target:
            return n

        seen.add(tuple(state))

        for b in buttons:
            next_state = list(state)
            for i in b:
                next_state[i] = 1 - next_state[i]

            q.append((n + 1, next_state))


def configure_joltage(target, buttons):
    # Not a fan of advent of math so I did not solve part 2 on my own.
    n = len(target)
    m = len(buttons)

    problem = pulp.LpProblem("Joltage_Configuration", pulp.LpMinimize)
    x_vars = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(m)]
    problem += pulp.lpSum(x_vars), "Total_Presses"
    
    for i in range(n):
        constraint_expr = pulp.lpSum(x_vars[j] for j in range(m) if i in buttons[j])
        problem += constraint_expr == target[i], f"Counter_{i}"
    
    solver = pulp.PULP_CBC_CMD(msg=False)
    problem.solve(solver)
    
    if pulp.LpStatus[problem.status] == 'Optimal':
        return sum(int(pulp.value(var)) for var in x_vars)


def parse(data):
    buttons = []
    targets = []
    joltages = []
    for l in data:
        parts = l.split(" ")
        target = []
        for ch in parts[0][1:-1]:
            if ch == '#':
                target.append(1)
            else:
                target.append(0)
        targets.append(target)

        current_buttons = []
        for item in parts[1:-1]:
            button = []
            for ch in item[1:-1].split(','):
                button.append(int(ch))
            current_buttons.append(button)
        buttons.append(current_buttons)

        for item in parts[-1:]:
            j = []
            for ch in item[1:-1].split(','):
                j.append(int(ch))
            joltages.append(j)
    return targets, buttons, joltages


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
