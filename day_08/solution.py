#!/bin/python3

import sys
from collections import defaultdict
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

    height = len(lines)
    width = len(lines[0])

    mapping = {}
    antennas_list = defaultdict(list)
    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            mapping[(row, col)] = cell
            if cell != ".":
                antennas_list[cell].append((row, col))

    antinodes = set()
    tested = set()
    for antenna in antennas_list:
        if len(antenna) > 1:
            for a1 in antenna:
                for a2 in antenna:
                    if a1 == a2:
                        continue

                    if (a1, a2) in tested or (a2, a1) in tested:
                        continue

                    tested.add((a1, a2))

                    # Calculate distance
                    dx = a1[1] - a2[1]
                    dy = a1[0] - a2[0]

                    anti_one = (a1[0], a1[1] + dx)
                    anti_two = (a2[0], a2[1] - dx)

                    anti_one = (anti_one[0] + dy, anti_one[1])
                    anti_two = (anti_two[0] - dy, anti_two[1])

                    if (
                        anti_one[0] >= 0
                        and anti_one[0] < height
                        and anti_one[1] >= 0
                        and anti_one[1] < width
                    ):
                        antinodes.add(anti_one)

                    if (
                        anti_two[0] >= 0
                        and anti_two[0] < height
                        and anti_two[1] >= 0
                        and anti_two[1] < width
                    ):
                        antinodes.add(anti_two)

    answer = len(antinodes)
    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    height = len(lines)
    width = len(lines[0])

    mapping = {}
    antennas_list = defaultdict(list)
    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            mapping[(row, col)] = cell
            if cell != ".":
                antennas_list[cell].append((row, col))

    antinodes = set()
    tested = set()

    for antenna in antennas_list:
        if len(antenna) > 1:
            for a1 in antenna:
                for a2 in antenna:
                    if a1 == a2:
                        continue

                    if (a1, a2) in tested or (a2, a1) in tested:
                        continue

                    tested.add((a1, a2))

                    # Calculate distance
                    dx = a1[1] - a2[1]
                    dy = a1[0] - a2[0]

                    # Basically just make antinodes on the slope of the line in both directions
                    # until we go OOB.
                    for prev in [a1, a2]:
                        for sign in [-1, 1]:
                            while True:
                                new_node = (
                                    prev[0] + (sign * dy),
                                    prev[1] + (sign * dx),
                                )

                                if (
                                    new_node[0] >= 0
                                    and new_node[0] < height
                                    and new_node[1] >= 0
                                    and new_node[1] < width
                                ):
                                    antinodes.add(new_node)
                                else:
                                    break

                                prev = new_node

    answer = len(antinodes)

    print(f"Part 2: {answer}")


part_one()
part_two()
