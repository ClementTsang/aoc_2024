#!/bin/python3

import re
import sys
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(line)

    return lines


def part_one():
    lines = read_lines_to_list()
    answer = 0

    for line in lines:
        muls = re.findall(r"mul\(\d+,\d+\)", line)
        for mul in muls:
            s = mul.split("(")[-1][:-1]
            [a, b] = s.split(",")
            answer += int(a) * int(b)

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    is_enabled = True
    for line in lines:
        instructions: List[str] = re.findall(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))", line)
        for inst in instructions:
            if inst == "do()":
                is_enabled = True
            elif inst == "don't()":
                is_enabled = False
            elif inst.startswith("mul"):
                if is_enabled:
                    s = inst.split("(")[-1][:-1]
                    [a, b] = s.split(",")
                    answer += int(a) * int(b)
            else:
                raise ("SOMETHING WENT WRONG AHHHH")

    print(f"Part 2: {answer}")


part_one()
part_two()
