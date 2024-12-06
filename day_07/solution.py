#!/bin/python3

import sys
from collections import Counter, defaultdict
from copy import deepcopy
from heapq import heappop, heappush
from typing import List, Set, Tuple

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # lines.append(list(line))
            lines.append(line)

    return lines


def part_one():
    lines = read_lines_to_list()
    answer = 0

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    print(f"Part 2: {answer}")


part_one()
part_two()
