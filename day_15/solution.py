#!/bin/python3

import sys
from collections import Counter, defaultdict
from copy import copy, deepcopy
from heapq import heappop, heappush
from typing import List, Set, Tuple

import multiprocess as mp
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

    mapping = dict()
    start = None
    instructions = []

    is_maze = True
    height = 0
    width = 0

    for i, line in enumerate(lines):
        if len(line.strip()) == 0:
            is_maze = False
            continue

        if is_maze:
            height += 1
            width = len(list(line))
            for j, cell in enumerate(list(line)):
                if cell == "@":
                    start = (i, j)
                mapping[(i, j)] = cell
        else:
            for inst in list(line):
                instructions.append(inst)

    curr = start
    # print(instructions)
    for inst in instructions:
        # print(f"inst: {inst}")

        if inst == "<":
            target = (curr[0], curr[1] - 1)
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] == "O":
                    # Basically keep checking boulders in the direction
                    # until you hit a wall or empty spot

                    boulder_list = [target]
                    while True:
                        current_boulder = boulder_list[-1]
                        to_check = (current_boulder[0], current_boulder[1] - 1)
                        if to_check not in mapping or mapping[to_check] == "#":
                            boulder_list = []
                            break
                        elif mapping[to_check] == "O":
                            boulder_list.append(to_check)
                        elif mapping[to_check] == ".":
                            break

                    if boulder_list:
                        for boulder in boulder_list:
                            mapping[(boulder[0], boulder[1] - 1)] = "O"
                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        elif inst == ">":
            target = (curr[0], curr[1] + 1)
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] == "O":
                    # Basically keep checking boulders in the direction
                    # until you hit a wall or empty spot

                    boulder_list = [target]
                    while True:
                        current_boulder = boulder_list[-1]
                        to_check = (current_boulder[0], current_boulder[1] + 1)
                        if to_check not in mapping or mapping[to_check] == "#":
                            boulder_list = []
                            break
                        elif mapping[to_check] == "O":
                            boulder_list.append(to_check)
                        elif mapping[to_check] == ".":
                            break
                    if boulder_list:
                        for boulder in boulder_list:
                            mapping[(boulder[0], boulder[1] + 1)] = "O"
                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        elif inst == "^":
            target = (curr[0] - 1, curr[1])
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] == "O":
                    # Basically keep checking boulders in the direction
                    # until you hit a wall or empty spot

                    boulder_list = [target]
                    while True:
                        current_boulder = boulder_list[-1]
                        to_check = (current_boulder[0] - 1, current_boulder[1])
                        if to_check not in mapping or mapping[to_check] == "#":
                            boulder_list = []
                            break
                        elif mapping[to_check] == "O":
                            boulder_list.append(to_check)
                        elif mapping[to_check] == ".":
                            break

                    if boulder_list:
                        for boulder in boulder_list:
                            mapping[(boulder[0] - 1, boulder[1])] = "O"
                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        elif inst == "v":
            target = (curr[0] + 1, curr[1])
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] == "O":
                    # Basically keep checking boulders in the direction
                    # until you hit a wall or empty spot

                    boulder_list = [target]
                    while True:
                        current_boulder = boulder_list[-1]
                        to_check = (current_boulder[0] + 1, current_boulder[1])
                        if to_check not in mapping or mapping[to_check] == "#":
                            boulder_list = []
                            break
                        elif mapping[to_check] == "O":
                            boulder_list.append(to_check)
                        elif mapping[to_check] == ".":
                            break

                    if boulder_list:
                        for boulder in boulder_list:
                            mapping[(boulder[0] + 1, boulder[1])] = "O"
                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        else:
            raise Exception("oops")

        # for i in range(height):
        #     for j in range(width):
        #         print(mapping[(i, j)], end="")
        #     print("")
        # print("")

    for coord, value in mapping.items():
        if value == "O":
            answer += 100 * coord[0] + coord[1]

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0
    mapping = dict()
    start = None
    instructions = []

    is_maze = True
    height = 0
    width = 0

    expanded_lines = []
    for line in lines:
        to_push = ""
        if len(line.strip()) == 0:
            is_maze = False
            expanded_lines.append("")

        if is_maze:
            for cell in list(line):
                if cell == "#":
                    to_push += "##"
                elif cell == "O":
                    to_push += "[]"
                elif cell == ".":
                    to_push += ".."
                elif cell == "@":
                    to_push += "@."
            expanded_lines.append(to_push)
        else:
            expanded_lines.append(line)

    # for l in expanded_lines:
    #     print(l)

    is_maze = True
    for i, line in enumerate(expanded_lines):
        if len(line.strip()) == 0:
            is_maze = False
            continue

        if is_maze:
            height += 1
            width = len(list(line))
            for j, cell in enumerate(list(line)):
                if cell == "@":
                    start = (i, j)
                mapping[(i, j)] = cell
        else:
            for inst in list(line):
                instructions.append(inst)

    curr = start
    # print(instructions)
    for inst in instructions:
        # print(f"inst: {inst}")

        if inst == "<":
            target = (curr[0], curr[1] - 1)
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] == "]":
                    pass

                    # Basically move pairs of boulders.
                    boulders = [((target[0], target[1] - 1), target)]
                    while True:
                        (left, right) = boulders[-1]
                        to_check_left = (left[0], left[1] - 2)
                        to_check_right = (left[0], left[1] - 1)

                        if to_check_left in mapping and to_check_right in mapping:
                            if mapping[to_check_right] == "#":
                                boulders = []
                                break
                            elif (
                                mapping[to_check_left] == "["
                                and mapping[to_check_right] == "]"
                            ):
                                boulders.append((to_check_left, to_check_right))
                                pass
                            elif mapping[to_check_right] == ".":
                                break
                        else:
                            boulders = []
                            break

                    if boulders:
                        for left_boulder, right_boulder in boulders:
                            mapping[(left_boulder[0], left_boulder[1] - 1)] = "["
                            mapping[(right_boulder[0], right_boulder[1] - 1)] = "]"
                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        elif inst == ">":
            target = (curr[0], curr[1] + 1)
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] == "[":
                    boulders = [(target, (target[0], target[1] + 1))]
                    while True:
                        (left, right) = boulders[-1]
                        to_check_left = (right[0], right[1] + 1)
                        to_check_right = (right[0], right[1] + 2)

                        if to_check_left in mapping and to_check_right in mapping:
                            if mapping[to_check_left] == "#":
                                boulders = []
                                break
                            elif (
                                mapping[to_check_left] == "["
                                and mapping[to_check_right] == "]"
                            ):
                                boulders.append((to_check_left, to_check_right))
                                pass
                            elif mapping[to_check_left] == ".":
                                break
                        else:
                            boulders = []
                            break

                    if boulders:
                        for left_boulder, right_boulder in reversed(boulders):
                            mapping[(right_boulder[0], right_boulder[1] + 1)] = "]"
                            mapping[(left_boulder[0], left_boulder[1] + 1)] = "["
                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        elif inst == "^":
            target = (curr[0] - 1, curr[1])
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] in "[]":
                    boulders = set([target])

                    to_explore = [target]
                    visited = set()
                    # Basically do a BFS/DFS to find all boxes we're touching.
                    while to_explore:
                        curr_boulder_char = to_explore.pop(0)
                        visited.add(curr_boulder_char)

                        # if it's touching a boulder character above it then add it, also find the boulder
                        # characters beside it that make it part of the boulder and add those too to test
                        # and as a boulder char

                        if mapping[curr_boulder_char] == "[":
                            curr_boulder_right = (
                                curr_boulder_char[0],
                                curr_boulder_char[1] + 1,
                            )
                            if curr_boulder_right not in visited:
                                to_explore.insert(0, curr_boulder_right)
                                boulders.add(curr_boulder_right)
                        else:
                            curr_boulder_left = (
                                curr_boulder_char[0],
                                curr_boulder_char[1] - 1,
                            )
                            if curr_boulder_left not in visited:
                                to_explore.insert(0, curr_boulder_left)
                                boulders.add(curr_boulder_left)

                        to_test = curr_boulder_char[0] - 1, curr_boulder_char[1]
                        if to_test in mapping:
                            if mapping[to_test] == ".":
                                continue
                            elif mapping[to_test] == "#":
                                boulders = set()
                                break
                            elif mapping[to_test] in "[]":
                                if to_test not in visited:
                                    to_explore.append(to_test)
                                    boulders.add(to_test)

                    boulders = list(boulders)
                    if boulders:
                        for boulder in sorted(boulders):
                            mapping[boulder[0] - 1, boulder[1]] = mapping[boulder]
                            mapping[boulder] = "."

                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target

        elif inst == "v":
            target = (curr[0] + 1, curr[1])
            if target in mapping:
                if mapping[target] == ".":
                    mapping[target] = "@"
                    mapping[curr] = "."
                    curr = target
                elif mapping[target] == "#":
                    # You hit a wall.
                    continue
                elif mapping[target] in "[]":
                    boulders = set([target])

                    to_explore = [target]
                    visited = set()
                    # Basically do a BFS/DFS to find all boxes we're touching.
                    while to_explore:
                        curr_boulder_char = to_explore.pop(0)
                        visited.add(curr_boulder_char)

                        # if it's touching a boulder character above it then add it, also find the boulder
                        # characters beside it that make it part of the boulder and add those too to test
                        # and as a boulder char

                        if mapping[curr_boulder_char] == "[":
                            curr_boulder_right = (
                                curr_boulder_char[0],
                                curr_boulder_char[1] + 1,
                            )
                            if curr_boulder_right not in visited:
                                to_explore.insert(0, curr_boulder_right)
                                boulders.add(curr_boulder_right)
                        else:
                            curr_boulder_left = (
                                curr_boulder_char[0],
                                curr_boulder_char[1] - 1,
                            )
                            if curr_boulder_left not in visited:
                                to_explore.insert(0, curr_boulder_left)
                                boulders.add(curr_boulder_left)

                        to_test = curr_boulder_char[0] + 1, curr_boulder_char[1]
                        if to_test in mapping:
                            if mapping[to_test] == ".":
                                continue
                            elif mapping[to_test] == "#":
                                boulders = set()
                                break
                            elif mapping[to_test] in "[]":
                                if to_test not in visited:
                                    to_explore.append(to_test)
                                    boulders.add(to_test)

                    boulders = list(boulders)
                    if boulders:
                        for boulder in reversed(sorted(boulders)):
                            mapping[boulder[0] + 1, boulder[1]] = mapping[boulder]
                            mapping[boulder] = "."

                        mapping[target] = "@"
                        mapping[curr] = "."
                        curr = target
        else:
            raise Exception("oops")

        # for i in range(height):
        #     for j in range(width):
        #         print(mapping[(i, j)], end="")
        #     print("")
        # print("")

    for coord, value in mapping.items():
        if value == "[":
            answer += 100 * coord[0] + coord[1]
    print(f"Part 2: {answer}")


part_one()
part_two()
