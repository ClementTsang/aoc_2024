#!/bin/python3

import sys
from typing import List

import networkx as nx

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(list(line))

    return lines


def solve(cheat_size: int) -> int:
    lines = read_lines_to_list()
    answer = 0

    start = None
    end = None

    walls = set()

    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            cheat_start = (i, j)
            if cell == "S":
                start = cheat_start
            elif cell == "E":
                end = cheat_start

            if cell == "#":
                walls.add((i, j))

    height = len(lines)
    width = len(lines[0])

    graph: nx.Graph = nx.grid_2d_graph(height, width)

    for wall in walls:
        graph.remove_node(wall)
    grid: nx.Graph = nx.grid_2d_graph(height, width)

    original_path = nx.shortest_path(graph, start, end)
    original = len(original_path) - 1

    tried = set()

    from_start = nx.single_source_dijkstra_path_length(graph, start)
    from_end = nx.single_source_dijkstra_path_length(graph, end)

    for i in range(height):
        for j in range(width):
            cheat_start = (i, j)

            if cheat_start not in graph:
                continue

            to_try = nx.single_source_dijkstra_path_length(
                grid, cheat_start, cutoff=cheat_size
            )
            for cheat_end, path_len in to_try.items():
                if cheat_end in graph.nodes and (cheat_start, cheat_end) not in tried:

                    tried.add((cheat_start, cheat_end))

                    result = from_start[cheat_start] + from_end[cheat_end] + path_len

                    diff = original - result

                    if diff >= 100:
                        answer += 1

    return answer


def part_one():
    print(f"Part 1: {solve(2)}")


def part_two():
    print(f"Part 2: {solve(20)}")


part_one()
part_two()
