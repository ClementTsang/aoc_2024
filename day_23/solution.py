#!/bin/python3

import sys
from typing import List

import networkx as nx

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

    connections = nx.Graph()
    for line in lines:
        [a, b] = line.split("-")
        connections.add_node(a)
        connections.add_node(b)

        connections.add_edge(a, b)
        connections.add_edge(b, a)

    results = set()
    for cycle in nx.simple_cycles(connections, 3):
        if len(cycle) != 3:
            continue

        if any(c.startswith("t") for c in cycle):
            cycle = sorted(cycle)
            results.add(tuple(cycle))

    answer = len(results)
    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    connections = nx.Graph()
    for line in lines:
        [a, b] = line.split("-")
        connections.add_node(a)
        connections.add_node(b)

        connections.add_edge(a, b)
        connections.add_edge(b, a)

    biggest_cycle = []
    for clique in nx.find_cliques(connections):
        if len(clique) > len(biggest_cycle):
            biggest_cycle = clique

    answer = ",".join(sorted(biggest_cycle))

    print(f"Part 2: {answer}")


part_one()
part_two()
