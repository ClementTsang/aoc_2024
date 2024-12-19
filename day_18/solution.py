#!/bin/python3

import sys
from typing import List

import networkx as nwx

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
GOAL = (70, 70) if "input.txt" in FILE else (6, 6)
STEPS = 1024 if "input.txt" in FILE else 12

# print(f"goal is {GOAL}, steps is {STEPS}")


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

    # in y, x
    coordinates = []

    for line in lines:
        xy = [int(i) for i in line.split(",")]
        coordinates.append((xy[1], xy[0]))

    graph = nwx.Graph()
    corrupted = set(coordinates[0:STEPS])
    for i in range(GOAL[0] + 1):
        for j in range(GOAL[1] + 1):
            if (i, j) not in corrupted:
                graph.add_node((i, j))

    for node in graph.nodes:
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            destination = node[0] + dy, node[1] + dx
            if destination in graph.nodes:
                graph.add_edge(node, destination)

    answer = nwx.shortest_path_length(graph, (0, 0), GOAL)

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    # in y, x
    coordinates = []

    for line in lines:
        xy = [int(i) for i in line.split(",")]
        coordinates.append((xy[1], xy[0]))

    graph = nwx.grid_2d_graph(GOAL[0] + 1, GOAL[1] + 1)

    # Possible optimizations:
    # - Binary search/use Python's bisect to narrow search space
    # - Only try checking path if the next coordinate lands on the current path
    #
    # But it runs in like 3 seconds so... eh.
    for steps in range(len(coordinates)):
        to_remove = coordinates[steps]
        graph.remove_node(to_remove)

        if not nwx.has_path(graph, (0, 0), GOAL):
            answer = coordinates[steps]
            answer = f"{answer[1]},{answer[0]}"
            break

    print(f"Part 2: {answer}")


part_one()
part_two()
