#!/bin/python3

import itertools
import sys
from copy import deepcopy
from typing import Dict, List, Tuple

from graphviz import Digraph

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(line)

    return lines


def solve(wires: Dict[str, int], gates: Dict[str, Tuple[str, ...]]) -> Dict:
    wires = deepcopy(wires)
    gates = list(gates.items())

    run = set()
    last_loop = None

    while gates:
        curr = gates.pop(0)

        if curr in run:
            continue

        (rhs, lhs) = curr
        (a, op, b) = lhs

        if a in wires and b in wires:
            run.add(curr)

            last_loop = None

            if op == "AND":
                wires[rhs] = wires[a] & wires[b]
            elif op == "OR":
                wires[rhs] = wires[a] | wires[b]
            elif op == "XOR":
                wires[rhs] = wires[a] ^ wires[b]
            else:
                raise Exception("bad op")
        else:
            if last_loop is None:
                last_loop = curr
            else:
                if last_loop == curr:
                    break
            gates.append(curr)

    return wires


def part_one():
    lines = read_lines_to_list()
    answer = 0

    is_wire = True
    wires = dict()
    gates = dict()

    for line in lines:
        if len(line) == 0:
            is_wire = False
            continue

        if is_wire:
            [wire, val] = line.split(": ")
            wires[wire] = int(val)
        else:
            [lhs, rhs] = line.split(" -> ")
            lhs = tuple(lhs.split())
            gates[rhs] = lhs

    wires = solve(wires, gates)

    result = []
    for k, v in wires.items():
        if k.startswith("z"):
            result.append((k, v))

    result.sort(reverse=True)
    answer = int("".join([str(b) for (a, b) in result]), 2)

    print(f"Part 1: {answer}")


def swap(gates, a, b):
    gates[a], gates[b] = gates[b], gates[a]


def draw(gates):
    dot = Digraph()

    for rhs, lhs in gates.items():
        if lhs[1] == "AND":
            color = "green"
        elif lhs[1] == "OR":
            color = "blue"
        elif lhs[1] == "XOR":
            color = "red"

        dot.edge(lhs[0], rhs, label=lhs[1], color=color)
        dot.edge(lhs[2], rhs, label=lhs[1], color=color)

    dot.render("day_24/graph", format="png")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    is_wire = True
    wires = dict()
    gates = dict()

    for line in lines:
        if len(line) == 0:
            is_wire = False
            continue

        if is_wire:
            [wire, val] = line.split(": ")
            wires[wire] = int(val)
        else:
            [lhs, rhs] = line.split(" -> ")
            lhs = tuple(lhs.split())
            gates[rhs] = lhs

    x_wires = [f"{b}" for (a, b) in wires.items() if a.startswith("x")]
    y_wires = [f"{b}" for (a, b) in wires.items() if a.startswith("y")]
    actual_val = int("".join(reversed(x_wires)), 2) + int("".join(reversed(y_wires)), 2)
    actual = (bin(actual_val)).split("b")[-1]

    correct = dict()
    final_z = list()
    for index, a in enumerate(actual):
        key = f"z{str(index).zfill(2)}"
        correct[key] = int(a)
        final_z.append(a)
    print(f"target: {''.join(final_z)}")

    swaps = [("dsd", "z37"), ("z19", "sbg"), ("z12", "djg"), ("hjm", "mcq")]
    for a, b in swaps:
        swap(gates, a, b)

    # draw(gates)

    wires = solve(wires, gates)

    result = []
    for k, v in wires.items():
        if k.startswith("z"):
            result.append((k, v))

    result.sort(reverse=True)
    print(f"actual: {''.join([str(b) for (a, b) in result])}")

    answer = ",".join(sorted(itertools.chain.from_iterable(swaps)))
    print(f"Part 2: {answer}")


part_one()
part_two()
