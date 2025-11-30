#!/usr/bin/env python3

import helpers
from collections import defaultdict, deque
import itertools


def part1(data):
    # It's not pretty, and it will only work for my input.
    program = [int(x) for x in data[0].split(",")]
    comp = Computer(program)

    safe_items = [
        "take asterisk\n",
        "take antenna\n",
        "take easter egg\n",
        "take space heater\n",
        "take jam\n",
        "take festive hat\n",
        "take fixed point\n",
        "take tambourine\n",
    ]

    drop_items = [
        "drop asterisk\n",
        "drop antenna\n",
        "drop easter egg\n",
        "drop space heater\n",
        "drop jam\n",
        "drop festive hat\n",
        "drop fixed point\n",
        "drop tambourine\n",
    ]

    commands = [
        "south\n",
        "south\n",
        "south\n",
        "south\n",
        "east\n",
        "west\n",
        "west\n",
        "west\n",
        "west\n",
        "south\n",
        "north\n",
        "east\n",
        "east\n",
        "north\n",
        "west\n",
        "west\n",
        "east\n",
        "north\n",
        "west\n",
        "north\n",
        "north\n",
        "south\n",
        "south\n",
        "east\n",
        "north\n",
        "west\n",
        "south\n",
        "north\n",
        "west\n",
        "south\n",
        "north\n",
        "west\n",
        "west\n",
    ]

    command = None
    while True:
        if command is not None:
            comp.input([ord(ch) for ch in command])
            comp.input([10])

        for item in safe_items:
            comp.input([ord(ch) for ch in item])
            message = run(comp)

        message = run(comp)
        if len(commands) == 0:
            break
        command = commands.pop(0)

    for item in drop_items:
        comp.input([ord(ch) for ch in item])


    message = run(comp)
    
    answer = None
    item_combinations = all_combinations(safe_items)
    for combo in item_combinations:
        for item in combo:
            comp.input([ord(ch) for ch in item])
            message = run(comp)

        command = "west\n"
        comp.input([ord(ch) for ch in command])
        message = run(comp)
        if "proceed" in message:
            answer = int(message.split()[55])
            break

        for item in drop_items:
            comp.input([ord(ch) for ch in item])

    print(f"\nPart 1: {answer}")



def run(comp):
    message = ""
    while True:
        out = comp.run_until_output()
        if out is None:
            break

        message += chr(out)
    return message


def all_combinations(items):
    result = []
    for r in range(1, len(items) + 1):  # Loop through lengths 1 to len(items)
        combinations = itertools.combinations(items, r)
        result.extend(combinations)
    return result

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
