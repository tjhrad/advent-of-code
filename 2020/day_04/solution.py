#!/usr/bin/env python3

import sys
import time
from helpers import format_time, read_input


def part1(data):
    requirements = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    passports = parse(data)
    answer = sum([1 for p in passports.values() if valid_passport(p, requirements)])
    print(f"\nPart 1: {answer}")


def part2(data):
    requirements = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    passports = parse(data)
    answer = sum([1 for p in passports.values() if valid_passport2(p, requirements)])
    print(f"\nPart 2: {answer}")


def valid_passport(passport, requirements):
    for r in requirements:
        if r == 'cid':
            continue
        if r not in passport:
            return False
    return True


def valid_passport2(passport, requirements):
    for r in requirements:
        if r == 'cid':
            continue

        if r not in passport:
            return False

        if r == 'byr' and not (1920 <= int(passport[r]) <= 2002):
            return False
        elif r == 'iyr' and not (2010 <= int(passport[r]) <= 2020):
            return False
        elif r == 'eyr' and not (2020 <= int(passport[r]) <= 2030):
            return False
        elif r == 'hgt':
            if passport[r].endswith('cm'):
                if not (150 <= int(passport[r][:-2]) <= 193):
                    return False
            elif passport[r].endswith('in'):
                if not (59 <= int(passport[r][:-2]) <= 76):
                    return False
            else:
                return False
        elif r == 'hcl':
            if passport[r][0] != '#' or len(passport[r]) != 7:
                return False
            for ch in passport[r][1:]:
                if ch not in '0123456789abcdef':
                    return False
        elif r == 'ecl':
            if passport[r] not in {'amb','blu','brn','gry','grn','hzl','oth'}:
                return False
        elif r == 'pid':
            if not passport[r].isdigit():
                return False
            elif len(passport[r]) != 9:
                return False
    return True


def parse(data):
    passports = dict()
    current = dict()
    n = 0
    for i in range(len(data)):
        if ':' in data[i]:
            items = data[i].split()
            for item in items:
                k, v = item.split(":")
                current[k] = v
        else:
            passports[n] = current
            n += 1
            current = dict()
    passports[n] = current
    n += 1
    return passports


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    try:
        data = read_input(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
        return

    start_time = time.time()
    part1(data)
    print(format_time(time.time() - start_time))

    start_time = time.time()
    part2(data)
    print(format_time(time.time() - start_time))


if __name__ == "__main__":
    main()
