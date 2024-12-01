#!/bin/python3

import sys
from collections import Counter
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

    left = []
    right = []
    for l in lines:
        [a, b] = l.split()
        left.append(int(a))
        right.append(int(b))
    left.sort()
    right.sort()

    answer = sum(abs(l - r) for (l, r) in zip(left, right))

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()

    left = []
    right = []
    for l in lines:
        [a, b] = l.split("   ")
        left.append(int(a))
        right.append(int(b))

    answer = 0
    right = Counter(right)
    for a in left:
        answer += a * right[a]

    print(f"Part 2: {answer}")


part_one()
part_two()
