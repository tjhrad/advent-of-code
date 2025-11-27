#!/usr/bin/env python3

import helpers
from collections import defaultdict, deque


def part1(data):
    program = [int(x) for x in data[0].split(",")]
    start = find_start(program)
    grid, answer = beam_size(program, start, 50)
    print(f"\nPart 1: {answer}")


def part2(data):
    program = [int(x) for x in data[0].split(",")]
    start = find_start(program)
    answer = fit_ship(program)
    print(f"\nPart 2: {answer}")


def find_start(program):
    start = None
    for y in range(1, 50):
        for x in range(1, 50):
            if start is not None:
                break
            computer = Computer(program)
            computer.input([x, y])
            out = computer.run_until_output()
            if out == 1:
                start = (x, y)
        if start is not None:
            break
    return start


def beam_size(program, start, size):
    count = 0
    grid = {}
    grid[(0, 0)] = 1

    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    q = deque([start])
    seen = set()

    while q:
        (x, y) = q.popleft()
        grid[(x, y)] = 1
        count += 1

        for dx, dy in dirs:
            nx, ny = x+dx, y+dy

            if (nx, ny) in seen:
                continue

            if nx >= size or ny >= size:
                continue

            seen.add((nx, ny))

            computer = Computer(program)
            computer.input([nx, ny])
            out = computer.run_until_output()
            if out == 1:
                q.append((nx, ny))

    return grid, count


def fit_ship(program, size=100):
    y = size
    x_L = 0

    while True:
        while True:
            com = Computer(program)
            com.input([x_L, y])
            if com.run_until_output() == 1:
                break
            x_L += 1

        x_check = x_L + size - 1
        y_check = y - size + 1
        com = Computer(program)
        com.input([x_check, y_check])

        if com.run_until_output() == 1:
            x = x_L
            y_start = y_check

            return (x * 10_000) + y_start

        y += 1


def print_grid(grid):
    if not grid:
        print("empty grid")
        return

    xs = [x for x, _ in grid.keys()]
    ys = [y for _, y in grid.keys()]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    for y in range(ymin, ymax + 1):
        row = ""
        for x in range(xmin, xmax + 1):
            if (x, y) in grid and grid[(x, y)] == 1:
                row += "#"
            else:
                row += "."
        print(row)


class Computer:
    def __init__(self, program):
        self.program: Dict[int, int] = defaultdict(int)
        for i, v in enumerate(program):
            self.program[i] = v

        self.ip:int = 0
        self.relative_base:int = 0
        self.output: int | None = None
        self.halted: bool = False
        self.input_queue: list[int] = []

    def input(self, input_list):
        for i in input_list:
            self.input_queue.append(i)

    def run_until_output(self):
        while True:
            mult_instruct = str(self.program[self.ip]).zfill(5)
            op = int(mult_instruct[-2:])
            modes = [int(mult_instruct[-3]), int(mult_instruct[-4]), int(mult_instruct[-5])]
            self.output = None

            def get_param(offset):
                val = self.program[self.ip + offset]
                if modes[offset - 1] == 0:   # position mode
                    return self.program[val]
                elif modes[offset - 1] == 1: # immediate mode
                    return val
                elif modes[offset - 1] == 2: # relative mode
                    return self.program[self.relative_base + val]

                raise ValueError(f"Unknown parameter mode")

            def get_write_addr(offset):
                val = self.program[self.ip + offset]
                return val if modes[offset - 1] == 0 else self.relative_base + val

            if op == 99:
                self.halted = True
                return None

            elif op == 1:  # add
                self.program[get_write_addr(3)] = get_param(1) + get_param(2)
                self.ip += 4

            elif op == 2:  # multiply
                self.program[get_write_addr(3)] = get_param(1) * get_param(2)
                self.ip += 4

            elif op == 3:  # input
                if len(self.input_queue) == 0:
                    return None
                self.program[get_write_addr(1)] = self.input_queue.pop(0)
                self.ip += 2

            elif op == 4:  # output
                self.output = get_param(1)
                self.ip += 2
                return self.output

            elif op == 5:  # jump-if-true
                self.ip = get_param(2) if get_param(1) != 0 else self.ip + 3

            elif op == 6:  # jump-if-false
                self.ip = get_param(2) if get_param(1) == 0 else self.ip + 3

            elif op == 7:  # less than
                self.program[get_write_addr(3)] = 1 if get_param(1) < get_param(2) else 0
                self.ip += 4

            elif op == 8:  # equals
                self.program[get_write_addr(3)] = 1 if get_param(1) == get_param(2) else 0
                self.ip += 4

            elif op == 9:  # adjust relative base
                self.relative_base += get_param(1)
                self.ip += 2

            else:
                raise ValueError(f"Unknown opcode {op} at position {self.ip}")


with open("./input.txt", "r") as f:
    data = [line.rstrip('\n') for line in f]


helpers.time_it(part1, data)
helpers.time_it(part2, data)
