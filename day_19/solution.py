#!/bin/python3

import sys
from functools import cache
from typing import List

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(line)

    return lines


def possible(design: str, patterns: List[str]) -> bool:
    if design == "":
        return True

    return any(
        (
            possible(design[len(pattern) :], patterns)
            if design.startswith(pattern)
            else False
        )
        for pattern in patterns
    )


def part_one():
    lines = read_lines_to_list()
    answer = 0

    patterns = lines[0].split(", ")
    designs = []

    for line in lines[2:]:
        if len(line.strip()) > 0:
            designs.append(line)

    for design in designs:
        if possible(design, patterns):
            answer += 1

    print(f"Part 1: {answer}")


def possible_two(design: str, patterns: List[str]) -> int:
    @cache
    def inner_possible_two(design: str) -> int:
        if design == "":
            return 1

        result = 0
        for pattern in patterns:
            if design.startswith(pattern):
                result += inner_possible_two(design[len(pattern) :])

        return result

    return inner_possible_two(design)


def part_two():
    lines = read_lines_to_list()
    answer = 0

    patterns = lines[0].split(", ")
    designs = []

    for line in lines[2:]:
        if len(line.strip()) > 0:
            designs.append(line)

    patterns = frozenset(patterns)
    for design in designs:
        results = possible_two(design, patterns)
        answer += results

    print(f"Part 2: {answer}")


part_one()
part_two()
