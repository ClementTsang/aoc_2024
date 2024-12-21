#!/bin/python3

import itertools
import sys
from collections import Counter
from functools import cache
from typing import List, Tuple

import networkx as nx

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(list(line))

    return lines


def create_numeric() -> nx.Graph:
    keypad = nx.Graph()
    kpl = [list("789"), list("456"), list("123"), [None, "0", "A"]]

    for i in range(len(kpl)):
        for j in range(len(kpl[i])):
            curr = kpl[i][j]

            if curr is None:
                continue

            keypad.add_node(curr)

    for i in range(len(kpl)):
        for j in range(len(kpl[i])):
            curr = kpl[i][j]

            if curr is None:
                continue

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_y, new_x = i + dy, j + dx
                if (
                    new_y >= 0
                    and new_y < len(kpl)
                    and new_x >= 0
                    and new_x < len(kpl[i])
                ):
                    neighbour = kpl[new_y][new_x]
                    if neighbour is None:
                        continue

                    keypad.add_edge(curr, neighbour)

    return keypad


@cache
def get_directions(curr: str, target: str) -> Tuple[str, ...]:
    """
    Return the most optimal way of moving between one cell and another.
    """

    # Screw it let's hard code this.
    if curr == target:
        return tuple("A")

    if curr == "A":
        if target == "^":
            path = "<A"
        elif target == "<":
            # no change
            path = "v<<A"
        elif target == "v":
            path = "<vA"
        elif target == ">":
            path = "vA"
    elif curr == "^":
        if target == "A":
            path = ">A"
        elif target == "<":
            # no change
            path = "v<A"
        elif target == "v":
            path = "vA"
        elif target == ">":
            path = "v>A"
    elif curr == "<":
        if target == "A":
            # no change
            path = ">>^A"
        elif target == "^":
            # no change
            path = ">^A"
        elif target == "v":
            path = ">A"
        elif target == ">":
            # no change
            path = ">>A"
    elif curr == "v":
        if target == "A":
            path = "^>A"
        elif target == "^":
            path = "^A"
        elif target == "<":
            path = "<A"
        elif target == ">":
            path = ">A"
    elif curr == ">":
        if target == "A":
            path = "^A"
        elif target == "^":
            path = "<^A"
        elif target == "<":
            # no change
            path = "<<A"
        elif target == "v":
            path = "<A"

    return tuple(path)


@cache
def solve_segment(
    segment: Tuple[str, ...],
) -> List[Tuple[str, ...]]:
    segment_moves = []
    curr = "A"
    for target in segment:
        path = get_directions(curr, target)
        curr = target
        segment_moves.append(path)
    return segment_moves


def solve_numeric(line: List[str], numeric: nx.Graph) -> List[List[str]]:
    curr = "A"
    ret = []

    for target in line:
        paths_from = list(nx.all_shortest_paths(numeric, curr, target))
        curr = target

        first_robot = []
        for path_from in paths_from:

            path = []
            for i in range(len(path_from) - 1):
                start = path_from[i]
                end = path_from[i + 1]

                if start == "A":
                    if end == "3":
                        path.append("^")
                    else:
                        path.append("<")
                elif end == "A":
                    if start == "3":
                        path.append("v")
                    else:
                        path.append(">")
                else:
                    start = int(start)
                    end = int(end)
                    if abs(start - end) == 1:
                        if start > end:
                            path.append("<")
                        else:
                            path.append(">")
                    else:
                        if start > end:
                            path.append("v")
                        else:
                            path.append("^")
            path.append("A")
            first_robot.append(tuple(path))
        ret.append(first_robot)

    out = list(list(tuple(vs) for vs in v) for v in itertools.product(*ret))
    return out


def update(counter: Counter) -> Counter:
    new_counter = Counter()

    for segment, amount in counter.items():
        new_segments = solve_segment(segment)
        for result in new_segments:
            new_counter[result] += amount

    return new_counter


def part_one():
    lines = read_lines_to_list()
    answer = 0

    numeric = create_numeric()

    for line in lines:
        code = "".join(line)
        numeric_value = int(code[:-1])

        best_length = 999999999999999999

        for first_robot in solve_numeric(line, numeric):
            counter = Counter(first_robot)

            counter = update(counter)  # second robot
            counter = update(counter)  # you

            length = sum(len(segment) * number for (segment, number) in counter.items())

            if length < best_length:
                best_length = length

        # print(code, numeric_value, best_length, best_length * numeric_value)
        answer += best_length * numeric_value

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    numeric = create_numeric()

    for line in lines:
        code = "".join(line)
        numeric_value = int(code[:-1])

        best_length = 999999999999999999
        for first_robot in solve_numeric(line, numeric):

            counter = Counter(first_robot)
            for _i in range(25):
                counter = update(counter)

            length = sum(len(segment) * number for (segment, number) in counter.items())

            if length < best_length:
                best_length = length

        answer += best_length * numeric_value

    print(f"Part 2: {answer}")


part_one()
part_two()
