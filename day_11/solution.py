#!/bin/python3

import sys
from collections import Counter, defaultdict
from copy import deepcopy
from heapq import heappop, heappush
from typing import List, Set, Tuple

import multiprocess as mp
import numpy as np

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def demo_z3_solver():
    # Who needs to think when you can z3
    import z3

    lines = read_lines_to_list()
    answer = 0

    solver = z3.Solver()
    x, y, z, vx, vy, vz = [
        z3.BitVec(var, 64) for var in ["x", "y", "z", "vx", "vy", "vz"]
    ]

    # 4 unknowns, so we just need 4 equations... I think.
    for itx in range(4):
        (cpx, cpy, cpz), (cvx, cvy, cvz) = lines[itx]

        t = z3.BitVec(f"t{itx}", 64)
        solver.add(t >= 0)
        solver.add(x + vx * t == cpx + cvx * t)
        solver.add(y + vy * t == cpy + cvy * t)
        solver.add(z + vz * t == cpz + cvz * t)

    if solver.check() == z3.sat:
        model = solver.model()
        (x, y, z) = (model.eval(x), model.eval(y), model.eval(z))
        answer = x.as_long() + y.as_long() + z.as_long()


def demo_network():
    from networkx import Graph, connected_components, minimum_edge_cut

    lines = read_lines_to_list()
    answer = 1

    graph = Graph()

    for node, connections in lines:
        graph.add_node(node)
        for connection in connections:
            graph.add_node(connection)
            graph.add_edge(
                *((node, connection) if node > connection else (connection, node))
            )

    cut = minimum_edge_cut(graph)
    graph.remove_edges_from(cut)

    components = connected_components(graph)
    for component in components:
        answer *= len(component)


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # lines.append(list(line))
            lines.append(line)

    return lines


def part_one():
    lines = read_lines_to_list()
    answer = 0

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    print(f"Part 2: {answer}")


part_one()
part_two()
