#!/bin/python3

import sys
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(list(line))

    return lines


def part_one():
    lines = read_lines_to_list()
    answer = 0

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if lines[row][col] == "X":
                if (
                    row >= 3
                    and lines[row - 1][col] == "M"
                    and lines[row - 2][col] == "A"
                    and lines[row - 3][col] == "S"
                ):
                    answer += 1

                if (
                    row < (len(lines) - 3)
                    and lines[row + 1][col] == "M"
                    and lines[row + 2][col] == "A"
                    and lines[row + 3][col] == "S"
                ):
                    answer += 1

                if (
                    col >= 3
                    and lines[row][col - 1] == "M"
                    and lines[row][col - 2] == "A"
                    and lines[row][col - 3] == "S"
                ):
                    answer += 1

                if (
                    col < (len(lines[0]) - 3)
                    and lines[row][col + 1] == "M"
                    and lines[row][col + 2] == "A"
                    and lines[row][col + 3] == "S"
                ):
                    answer += 1

                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if (
                            row + i * 3 < len(lines)
                            and col + j * 3 < len(lines[0])
                            and row + i * 3 >= 0
                            and col + j * 3 >= 0
                            and lines[row + i][col + j] == "M"
                            and lines[row + i * 2][col + j * 2] == "A"
                            and lines[row + i * 3][col + j * 3] == "S"
                        ):
                            answer += 1

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if lines[row][col] == "A":
                if (
                    row - 1 >= 0
                    and col - 1 >= 0
                    and col + 1 < len(lines[0])
                    and row + 1 < len(lines)
                ):
                    top_left = lines[row - 1][col - 1]
                    top_right = lines[row - 1][col + 1]
                    bottom_left = lines[row + 1][col - 1]
                    bottom_right = lines[row + 1][col + 1]

                    valid_to_right = (top_left == "M" and bottom_right == "S") or (
                        top_left == "S" and bottom_right == "M"
                    )
                    valid_to_left = (top_right == "M" and bottom_left == "S") or (
                        top_right == "S" and bottom_left == "M"
                    )

                    if valid_to_right and valid_to_left:
                        answer += 1

    print(f"Part 2: {answer}")


part_one()
part_two()
