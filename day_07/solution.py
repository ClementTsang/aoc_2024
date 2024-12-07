#!/bin/python3

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

    equations = []

    for line in lines:
        [test, right] = line.split(":")
        test = int(test)
        values = [int(v) for v in right.strip().split()]

        equations.append((test, values))

    for test, values in equations:

        def try_solving(lhs: int | float, rhs: List[int]):
            if isinstance(lhs, float) and not lhs.is_integer():
                return False

            lhs = int(lhs)

            if len(rhs) == 0:
                if lhs == 0:
                    return True
                else:
                    return False

            return try_solving(lhs - rhs[-1], rhs[:-1]) or try_solving(
                lhs / rhs[-1], rhs[:-1]
            )

        if try_solving(test, values):
            answer += test

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    equations = []

    for line in lines:
        [test, right] = line.split(":")
        test = int(test)
        values = [int(v) for v in right.strip().split()]

        equations.append((test, values))

    for test, values in equations:

        def try_solving(lhs: int, rhs: List[int], curr: str):
            if len(rhs) == 0:
                curr_lhs = 0
                curr_rhs = 0
                curr_operation = None
                for c in curr:
                    if c.isnumeric():
                        if curr_operation is None:
                            curr_lhs = curr_lhs * 10 + int(c)
                        else:
                            curr_rhs = curr_rhs * 10 + int(c)
                    elif c == "*":
                        if curr_operation is None:
                            curr_operation = "*"
                        else:
                            if curr_operation == "*":
                                curr_lhs = curr_lhs * curr_rhs
                            elif curr_operation == "|":
                                curr_lhs = int(str(curr_lhs) + str(curr_rhs))
                            else:
                                curr_lhs = curr_lhs + curr_rhs
                            curr_rhs = 0
                            curr_operation = "*"
                    elif c == "|":
                        if curr_operation is None:
                            curr_operation = "|"
                        else:
                            if curr_operation == "*":
                                curr_lhs = curr_lhs * curr_rhs
                            elif curr_operation == "|":
                                curr_lhs = int(str(curr_lhs) + str(curr_rhs))
                            else:
                                curr_lhs = curr_lhs + curr_rhs
                            curr_rhs = 0
                            curr_operation = "|"
                    elif c == "+":
                        if curr_operation is None:
                            curr_operation = "+"
                        else:
                            if curr_operation == "*":
                                curr_lhs = curr_lhs * curr_rhs
                            elif curr_operation == "|":
                                curr_lhs = int(str(curr_lhs) + str(curr_rhs))
                            else:
                                curr_lhs = curr_lhs + curr_rhs
                            curr_rhs = 0
                            curr_operation = "+"

                if curr_operation == "*":
                    curr_lhs = curr_lhs * curr_rhs
                elif curr_operation == "|":
                    curr_lhs = int(str(curr_lhs) + str(curr_rhs))
                else:
                    curr_lhs = curr_lhs + curr_rhs
                return curr_lhs == lhs

            if len(curr) == 0 and len(rhs) >= 2:
                return (
                    try_solving(lhs, rhs[2:], f"{rhs[0]}+{rhs[1]}")
                    or try_solving(lhs, rhs[2:], f"{rhs[0]}*{rhs[1]}")
                    or try_solving(lhs, rhs[2:], f"{rhs[0]}|{rhs[1]}")
                )
            elif len(curr) == 0 and len(rhs) == 1:
                return (
                    try_solving(lhs, rhs[2:], f"{rhs[0]}")
                    or try_solving(lhs, rhs[2:], f"{rhs[0]}")
                    or try_solving(lhs, rhs[2:], f"{rhs[0]}")
                )
            else:
                return (
                    try_solving(lhs, rhs[1:], f"{curr}+{rhs[0]}")
                    or try_solving(lhs, rhs[1:], f"{curr}*{rhs[0]}")
                    or try_solving(lhs, rhs[1:], f"{curr}|{rhs[0]}")
                )

        if try_solving(test, values, ""):
            answer += test

    print(f"Part 2: {answer}")


part_one()
part_two()
