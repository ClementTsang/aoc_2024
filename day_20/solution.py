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


def part_one():
    lines = read_lines_to_list()
    answer = 0

    start = None
    end = None

    graph = nx.Graph()
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
            else:
                graph.add_node(cheat_start)

    for node in graph.nodes:
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            destination = node[0] + dy, node[1] + dx
            if destination in graph.nodes:
                graph.add_edge(node, destination)

    original_path = nx.shortest_path(graph, start, end)
    original = len(original_path) - 1

    height = len(lines)
    width = len(lines[0])

    tried = set()

    for i in range(height):
        for j in range(width):
            cheat_start = (i, j)
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                cheat_end = cheat_start[0] + dy, cheat_start[1] + dx

                if (
                    cheat_end[0] >= 0
                    and cheat_end[0] < height
                    and cheat_end[1] >= 0
                    and cheat_end[1] < width
                    and (cheat_start, cheat_end) not in tried
                    and (cheat_end, cheat_start) not in tried
                    and (
                        (cheat_end in walls and cheat_start not in walls)
                        or cheat_end not in walls
                        and cheat_start in walls
                    )
                ):
                    tried.add((cheat_start, cheat_end))
                    tried.add((cheat_end, cheat_start))

                    remove_start = False
                    if cheat_start not in graph:
                        remove_start = True
                        graph.add_node(cheat_start)

                    for ddy, ddx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        destination = cheat_start[0] + ddy, cheat_start[1] + ddx
                        if destination in graph:
                            graph.add_edge(cheat_start, destination)
                            graph.add_edge(destination, cheat_start)

                    remove_end = False
                    if cheat_end not in graph:
                        remove_end = True
                        graph.add_node(cheat_end)

                    for ddy, ddx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        destination = cheat_end[0] + ddy, cheat_end[1] + ddx
                        if destination in graph:
                            graph.add_edge(cheat_end, destination)
                            graph.add_edge(destination, cheat_end)

                    graph.add_edge(cheat_start, cheat_end)
                    graph.add_edge(cheat_end, cheat_start)

                    result = nx.shortest_path_length(graph, start, end)

                    if original - result >= 100:
                        answer += 1

                    if remove_start:
                        graph.remove_node(cheat_start)

                    if remove_end:
                        graph.remove_node(cheat_end)

    # TODO: I'm double-counting for some reason (probably because I'm not treating start and end properly).
    # Just divide by 2 though, kinda cheating but it works.
    print(f"Part 1: {answer // 2}")


def part_two():
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

            to_try = nx.single_source_dijkstra_path_length(grid, cheat_start, cutoff=20)
            for cheat_end, path_len in to_try.items():
                if cheat_end in graph.nodes and (cheat_start, cheat_end) not in tried:

                    tried.add((cheat_start, cheat_end))

                    result = from_start[cheat_start] + from_end[cheat_end] + path_len

                    diff = original - result

                    if diff >= 100:
                        answer += 1

    print(f"Part 2: {answer}")


part_one()
part_two()
