#!/bin/python3

import sys
from typing import List

import numpy as np

sys.setrecursionlimit(100000)
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

    ams = []
    bms = []
    prizes = []
    for line in lines:
        if len(line.strip()) == 0:
            continue

        if line.startswith("Button A"):
            l = line.split(": ")[-1]
            l: List[str] = l.split(", ")
            x = int(l[0].strip("X+"))
            y = int(l[1].strip("Y+"))
            ams.append((x, y))
        elif line.startswith("Button B"):
            l = line.split(": ")[-1]
            l: List[str] = l.split(", ")
            x = int(l[0].strip("X+"))
            y = int(l[1].strip("Y+"))
            bms.append((x, y))
        else:
            l = line.split(": ")[-1]
            l: List[str] = l.split(", ")
            x = int(l[0].strip("X="))
            y = int(l[1].strip("Y="))
            prizes.append((x, y))

    for itx, (a, b, prize) in enumerate(zip(ams, bms, prizes)):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]

        target_x = prize[0]
        target_y = prize[1]

        one = np.array([[ax, bx], [ay, by]], dtype=np.uint32)
        two = np.array([target_x, target_y], dtype=np.uint32)

        result = np.linalg.solve(one, two)
        result = str(result)

        # Because I can't with numpy types
        if ". " in result and ".]" in result:
            left = result.split("[")[-1].split(".")[0]
            right = result.split(". ")[-1].split(".]")[0]
            tokens = int(left) * 3 + int(right)
            answer += tokens

    print(f"Part 1: {answer}")


def part_two():
    # It's z3 time again
    import z3

    lines = read_lines_to_list()
    answer = 0

    ams = []
    bms = []
    prizes = []
    for line in lines:
        if len(line.strip()) == 0:
            continue

        if line.startswith("Button A"):
            l = line.split(": ")[-1]
            l: List[str] = l.split(", ")
            x = int(l[0].strip("X+"))
            y = int(l[1].strip("Y+"))
            ams.append((x, y))
        elif line.startswith("Button B"):
            l = line.split(": ")[-1]
            l: List[str] = l.split(", ")
            x = int(l[0].strip("X+"))
            y = int(l[1].strip("Y+"))
            bms.append((x, y))
        else:
            l = line.split(": ")[-1]
            l: List[str] = l.split(", ")
            x = int(l[0].strip("X="))
            y = int(l[1].strip("Y="))
            prizes.append((x + 10000000000000, y + 10000000000000))

    for itx, (a, b, prize) in enumerate(zip(ams, bms, prizes)):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]

        target_x = prize[0]
        target_y = prize[1]

        solver = z3.Solver()
        (a, b) = z3.Ints("a b")
        solver.add(ax * a + bx * b == target_x)
        solver.add(ay * a + by * b == target_y)

        if solver.check() == z3.sat:
            model = solver.model()
            answer += model.eval(a).as_long() * 3 + model.eval(b).as_long()

    print(f"Part 2: {answer}")


part_one()
part_two()
