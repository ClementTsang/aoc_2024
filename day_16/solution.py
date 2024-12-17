#!/bin/python3

import sys
from typing import List

import networkx as nwx

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

    graph = nwx.DiGraph()
    start = None
    end = None

    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell == "#":
                continue
            if cell == "S":
                start = (i, j)
            elif cell == "E":
                end = (i, j)

            for direction in ["n", "e", "s", "w"]:
                graph.add_node(((i, j), direction))

    for node, direction in graph.nodes:
        if direction == "n":
            destination = (node[0] - 1, node[1])
        elif direction == "e":
            destination = (node[0], node[1] + 1)
        elif direction == "s":
            destination = (node[0] + 1, node[1])
        elif direction == "w":
            destination = (node[0], node[1] - 1)

        if (destination, direction) in graph.nodes:
            graph.add_edge((node, direction), (destination, direction), weight=1)

        for new_direction in ["n", "e", "s", "w"]:
            graph.add_edge((node, direction), (node, new_direction), weight=1000)

    for direction in ["n", "e", "s", "w"]:
        graph.add_edge((end, direction), "end", weight=0)

    answer = nwx.shortest_path_length(graph, (start, "e"), "end", weight="weight")

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()

    graph = nwx.DiGraph()
    start = None
    end = None

    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell == "#":
                continue
            if cell == "S":
                start = (i, j)
            elif cell == "E":
                end = (i, j)

            for direction in ["n", "e", "s", "w"]:
                graph.add_node(((i, j), direction))

    for node, direction in graph.nodes:
        if direction == "n":
            destination = (node[0] - 1, node[1])
        elif direction == "e":
            destination = (node[0], node[1] + 1)
        elif direction == "s":
            destination = (node[0] + 1, node[1])
        elif direction == "w":
            destination = (node[0], node[1] - 1)

        if (destination, direction) in graph.nodes:
            graph.add_edge((node, direction), (destination, direction), weight=1)

        for new_direction in ["n", "e", "s", "w"]:
            graph.add_edge((node, direction), (node, new_direction), weight=1000)

    for direction in ["n", "e", "s", "w"]:
        graph.add_edge((end, direction), "end", weight=0)

    paths = nwx.all_shortest_paths(graph, (start, "e"), "end", weight="weight")

    nodes = set()
    for path in paths:
        for node in path:
            if node != "end":
                nodes.add(node[0])

    answer = len(nodes)

    print(f"Part 2: {answer}")


part_one()
part_two()
