#!/bin/python3

import sys
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append([int(c) if c != "." else -100 for c in list(line)])

    return lines


def part_one():
    lines = read_lines_to_list()
    answer = 0

    starts = []
    height = len(lines)
    width = len(lines[0])

    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == 0:
                starts.append((row, col))

    for start in starts:
        queue = [start]
        visited = set()
        while queue:
            curr = queue.pop(0)
            val = lines[curr[0]][curr[1]]

            if val == 9:
                answer += 1
                continue

            if curr[0] - 1 >= 0 and lines[curr[0] - 1][curr[1]] - val == 1:
                if (curr[0] - 1, curr[1]) not in visited:
                    visited.add((curr[0] - 1, curr[1]))
                    queue.append((curr[0] - 1, curr[1]))
            if curr[0] + 1 < height and lines[curr[0] + 1][curr[1]] - val == 1:
                if (curr[0] + 1, curr[1]) not in visited:
                    visited.add((curr[0] + 1, curr[1]))
                    queue.append((curr[0] + 1, curr[1]))
            if curr[1] - 1 >= 0 and lines[curr[0]][curr[1] - 1] - val == 1:
                if (curr[0], curr[1] - 1) not in visited:
                    visited.add((curr[0], curr[1] - 1))
                    queue.append((curr[0], curr[1] - 1))
            if curr[1] + 1 < width and lines[curr[0]][curr[1] + 1] - val == 1:
                if (curr[0], curr[1] + 1) not in visited:
                    visited.add((curr[0], curr[1] + 1))
                    queue.append((curr[0], curr[1] + 1))

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    starts = []
    height = len(lines)
    width = len(lines[0])

    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == 0:
                starts.append((row, col))

    trails = set()

    for start in starts:
        queue = [(start, [])]
        while queue:
            (curr, prev) = queue.pop(0)
            val = lines[curr[0]][curr[1]]

            prev.append(curr)

            if val == 9:

                trails.add(frozenset((tuple(prev),)))
                continue

            if curr[0] - 1 >= 0 and lines[curr[0] - 1][curr[1]] - val == 1:
                queue.append(((curr[0] - 1, curr[1]), prev))
            if curr[0] + 1 < height and lines[curr[0] + 1][curr[1]] - val == 1:
                queue.append(((curr[0] + 1, curr[1]), prev))
            if curr[1] - 1 >= 0 and lines[curr[0]][curr[1] - 1] - val == 1:
                queue.append(((curr[0], curr[1] - 1), prev))
            if curr[1] + 1 < width and lines[curr[0]][curr[1] + 1] - val == 1:
                queue.append(((curr[0], curr[1] + 1), prev))

    answer = len(trails)
    print(f"Part 2: {answer}")


part_one()
part_two()
