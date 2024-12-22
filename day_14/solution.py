#!/bin/python3

import sys
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
HEIGHT = 7 if "input.txt" not in FILE else 103
WIDTH = 11 if "input.txt" not in FILE else 101

print(f"HEIGHT = {HEIGHT}, WIDTH = {WIDTH}")


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(line)

    return lines


def move_bot(width, height, positions, velocities):
    for i in range(len(positions)):
        position = positions[i]
        velocity = velocities[i]

        position[0] += velocity[0]
        while position[0] < 0:
            position[0] += width

        while position[0] >= width:
            position[0] -= width

        position[1] += velocity[1]
        while position[1] < 0:
            position[1] += height

        while position[1] >= height:
            position[1] -= height


def part_one():
    lines = read_lines_to_list()
    answer = 0

    positions = []
    velocities = []

    for line in lines:
        [p, v] = line.split(" ")
        p = [int(val) for val in p.split("=")[-1].split(",")]
        v = [int(val) for val in v.split("=")[-1].split(",")]

        positions.append(p)
        velocities.append(v)

    for _i in range(100):
        move_bot(WIDTH, HEIGHT, positions, velocities)

    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for position in positions:
        if position[0] < WIDTH // 2:
            if position[1] < HEIGHT // 2:
                q1 += 1
            elif position[1] > HEIGHT // 2:
                q2 += 1
        elif position[0] > WIDTH // 2:
            if position[1] < HEIGHT // 2:
                q3 += 1
            elif position[1] > HEIGHT // 2:
                q4 += 1
    answer = q1 * q2 * q3 * q4

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    positions = []
    velocities = []

    for line in lines:
        [p, v] = line.split(" ")
        p = [int(val) for val in p.split("=")[-1].split(",")]
        v = [int(val) for val in v.split("=")[-1].split(",")]

        positions.append(p)
        velocities.append(tuple(v))

    states = set()
    while True:
        answer += 1
        move_bot(WIDTH, HEIGHT, positions, velocities)

        positions_tuple = [(x, y) for [x, y] in positions]
        # A guess that we can clear it if we find any position where everything is used.
        if len(set(positions_tuple)) == len(positions_tuple):
            break

        state = frozenset((tuple(positions_tuple),))

        if state in states:
            break
        states.add(state)

    print(f"==== {answer} ====")
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if [j, i] in positions:
                print("█", end="")
            else:
                print(" ", end="")
        print("")

    print(f"Part 2: {answer}")


part_one()
part_two()
