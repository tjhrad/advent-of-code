#!/usr/bin/env python3

import helpers
from collections import defaultdict, deque


def part1(data):
    program = [int(x) for x in data[0].split(",")]
    computer = Computer(program)
    map, _ = get_map(computer)
    answer = sum_alignment_parameters(map)
    print(f"\nPart 1: {answer}")


def part2(data):
    program = [int(x) for x in data[0].split(",")]
    program[0] = 2
    computer = Computer(program)

    main_pattern = "A,B,A,C,B,A,C,B,A,C\n"
    a_pattern = "L,12,L,12,L,6,L,6\n"
    b_pattern = "R,8,R,4,L,12\n" 
    c_pattern = "L,12,L,6,R,12,R,8\n"

    [computer.input_queue.append(ord(c)) for c in main_pattern]
    [computer.input_queue.append(ord(c)) for c in a_pattern]
    [computer.input_queue.append(ord(c)) for c in b_pattern]
    [computer.input_queue.append(ord(c)) for c in c_pattern]
    computer.input_queue.append(ord('n'))
    computer.input_queue.append(ord('\n'))

    answer = 0
    while not computer.halted:
        out = computer.run_until_output()
        if out is not None:
            answer = out

    print(f"\nPart 2: {answer}")


def get_path(map, start):
    # I used this to then solve by hand based on the output
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    TURN_RIGHT = {(0, -1): (1, 0), (0, 1): (-1, 0), (-1, 0): (0, -1), (1, 0): (0, 1)}
    TURN_LEFT = {(0, -1): (-1, 0), (-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1)}

    def is_scaffold(p):
        return map.get(p, ".") in "#<>^vX"
    
    current_direction = DIRECTIONS[0]
    current_pos = start
    path = []

    while True:
        forward = (current_pos[0] + current_direction[0], current_pos[1] + current_direction[1])

        if is_scaffold(forward):
            steps = 0
            while is_scaffold(forward):
                current_pos = forward
                steps += 1
                forward = (current_pos[0] + current_direction[0], current_pos[1] + current_direction[1])
            path.append(steps)
        else:
            left_dir = TURN_LEFT[current_direction]
            left_pos = (current_pos[0] + left_dir[0], current_pos[1] + left_dir[1])
            if is_scaffold(left_pos):
                path.append("L")
                current_direction = left_dir
                continue

            right_dir = TURN_RIGHT[current_direction]
            right_pos = (current_pos[0] + right_dir[0], current_pos[1] + right_dir[1])
            if is_scaffold(right_pos):
                path.append("R")
                current_direction = right_dir
                continue

            break

    return path

        
    
def sum_alignment_parameters(map):
    xs = [x for x, _ in map.keys()]
    ys = [y for _, y in map.keys()]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    
    sum_of_parameters = 0
    for y in range(ymin, ymax + 1):
        if y == 0 or y == ymax:
            continue

        for x in range(xmin, xmax + 1):
            if x == 0 or x == xmax:
                continue

            if map[(x, y)] != "#":
                continue

            if map[(x+1, y)] == "#" and map[(x-1, y)] == "#" and map[(x, y+1)] == "#" and map[(x, y-1)] == "#":
                sum_of_parameters += (x*y)

    return sum_of_parameters


def get_map(computer):
    x = 0
    y = 0
    robot_pos = None
    map = defaultdict(str)
    while not computer.halted:
        out = computer.run_until_output()

        if out is None:
            continue

        if out == 35 or out == 60 or out == 62 or out == 94 or out == 118:
            map[(x, y)] = "#"
            if out == 60 or out == 62 or out == 94 or out == 118:
                robot_pos = (x, y)
            x += 1
        elif out == 46:
            map[(x, y)] = "."
            x += 1
        elif out == 10:
            y += 1
            x = 0
        else:
            print(f"Unknown out: {out}")

    return map, robot_pos


def print_map(graph):
    if not graph:
        print("empty map")
        return

    xs = [x for x, _ in graph.keys()]
    ys = [y for _, y in graph.keys()]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    for y in range(ymin, ymax + 1):
        row = ""
        for x in range(xmin, xmax + 1):
            if (x, y) in graph:
                row += graph[(x, y)]
            else:
                row += "?"
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
