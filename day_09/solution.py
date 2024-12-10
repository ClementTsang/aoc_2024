#!/bin/python3

import sys
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


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
    vals = [int(val) for val in list(lines[0])]
    answer = 0

    id = 0
    strip = []
    is_block = True
    for i in range(len(vals)):
        if is_block:
            strip.extend([id] * vals[i])
            id += 1
        else:
            strip.extend([None] * vals[i])

        is_block = not is_block

    free_space = strip.index(None)
    for i in reversed(range(0, len(strip))):
        if strip[i] is not None:
            strip[free_space] = strip[i]
            strip[i] = None
            while strip[free_space] is not None:
                free_space += 1
            if i - free_space <= 1:
                break

    answer = sum(val * itx if val is not None else 0 for (itx, val) in enumerate(strip))
    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    vals = [int(val) for val in list(lines[0])]
    answer = 0

    id = 0
    strip = []
    gaps = []
    blocks = []
    is_block = True
    for i in range(len(vals)):
        if is_block:
            blocks.append((len(strip), id, vals[i]))
            strip.extend([id] * vals[i])
            id += 1
        else:
            gaps.append((vals[i], len(strip)))
            strip.extend([None] * vals[i])

        is_block = not is_block

    # print("".join([str(v) if v is not None else "." for v in strip]))
    # print("".join(["o" if v is not None else "." for v in strip]))
    for block in reversed(blocks):
        (position, id, length) = block
        for itx, (gap_length, gap_position) in enumerate(gaps):
            if gap_position > position:
                break

            if gap_length >= length:
                for l in range(length):
                    strip[position + l] = None
                    strip[gap_position + l] = id

                diff = gap_length - length
                if diff > 0:
                    gaps[itx] = (diff, gap_position + length)
                else:
                    gaps.pop(itx)
                break
        # print("".join([str(v) if v is not None else "." for v in strip]))
    # print("".join(["o" if v is not None else "." for v in strip]))

    answer = sum(val * itx if val is not None else 0 for (itx, val) in enumerate(strip))

    print(f"Part 2: {answer}")


part_one()
part_two()
