#!/usr/bin/env python3

import helpers
from collections import defaultdict, deque


def part1(data):
    program = [int(x) for x in data[0].split(",")]
    com = Computer(program)

    springscript = [
        "NOT C J\n",
        "AND D J\n",
        "NOT A T\n",
        "OR T J\n",
        "WALK\n"
    ]

    for i in springscript:
        com.input([ord(c) for c in i])

    answer = run_program(com)
    print(f"\nPart 1: {answer}")


def part2(data):
    program = [int(x) for x in data[0].split(",")]
    com = Computer(program)

    springscript = [
        "NOT C J\n",
        "AND D J\n",
        "AND H J\n",
        "NOT B T\n",
        "AND D T\n",
        "OR T J\n",
        "NOT A T\n",
        "OR T J\n",
        "RUN\n"
    ]

    for i in springscript:
        com.input([ord(c) for c in i])

    answer = run_program(com)
    print(f"\nPart 2: {answer}")


def run_program(com):
    row = ""
    message = ""
    answer = None
    while not com.halted:
        out = com.run_until_output()
        if out is None:
            break

        if out > 255:
            return out

    return None


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
