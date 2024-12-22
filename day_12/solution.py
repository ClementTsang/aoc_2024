#!/bin/python3

import sys
from typing import List, Tuple

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(list(line))

    return lines


def grid_to_map(
    grid: List[List[str]],
) -> Tuple[Tuple[int, int], dict[Tuple[int, int], str]]:
    """
    Convert a mapping grind to a dict.

    Generics requires 3.12 or higher.
    """

    height = len(grid)
    width = len(grid[0])

    mapping = dict()
    for row in range(height):
        for col in range(width):
            mapping[(row, col)] = grid[row][col]

    return (height, width, mapping)


def part_one():
    lines = read_lines_to_list()
    answer = 0
    (height, width, mapping) = grid_to_map(lines)

    # Get all regions by flood searching.
    regions = set()
    visited = set()

    for row in range(height):
        for col in range(width):
            # There's a better way of doing this but I'm lazy.
            start = (row, col)
            if start in visited:
                continue

            symbol = mapping[start]

            to_visit_for_symbol = [start]
            visited_for_symbol = set()
            curr_region = set()

            while to_visit_for_symbol:
                curr = to_visit_for_symbol.pop()
                visited_for_symbol.add(curr)

                if mapping[curr] != symbol:
                    continue

                curr_region.add(curr)
                visited.add(curr)

                for i in [-1, 1]:
                    new_coords = (curr[0] + i, curr[1])

                    if (
                        new_coords in mapping
                        and mapping[new_coords] == symbol
                        and new_coords not in visited_for_symbol
                        and new_coords not in visited
                    ):
                        to_visit_for_symbol.append(new_coords)

                for i in [-1, 1]:
                    new_coords = (curr[0], curr[1] + i)

                    if (
                        new_coords in mapping
                        and mapping[new_coords] == symbol
                        and new_coords not in visited_for_symbol
                        and new_coords not in visited
                    ):
                        to_visit_for_symbol.append(new_coords)

            regions.add((symbol, frozenset(curr_region)))

    for symbol, region in regions:
        area = len(region)

        # How to find perimeter? Go through each coord in the region,
        # check all 4 directions, and add one for each non-matching symbol.

        perimeter = 0
        for coord in region:
            for i in [-1, 1]:
                to_check = (coord[0] + i, coord[1])
                if to_check not in mapping or mapping[to_check] != symbol:
                    perimeter += 1

            for i in [-1, 1]:
                to_check = (coord[0], coord[1] + i)
                if to_check not in mapping or mapping[to_check] != symbol:
                    perimeter += 1

        cost = area * perimeter
        # print(f"{symbol} -> area = {area}, perimeter = {perimeter}, cost = {cost}")

        answer += cost

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0
    (height, width, mapping) = grid_to_map(lines)

    # Get all regions by flood searching.
    regions = set()
    visited = set()

    for row in range(height):
        for col in range(width):
            # There's a better way of doing this but I'm lazy.
            start = (row, col)
            if start in visited:
                continue

            symbol = mapping[start]

            to_visit_for_symbol = [start]
            visited_for_symbol = set()
            curr_region = set()

            while to_visit_for_symbol:
                curr = to_visit_for_symbol.pop()
                visited_for_symbol.add(curr)

                if mapping[curr] != symbol:
                    continue

                curr_region.add(curr)
                visited.add(curr)

                for i in [-1, 1]:
                    new_coords = (curr[0] + i, curr[1])

                    if (
                        new_coords in mapping
                        and mapping[new_coords] == symbol
                        and new_coords not in visited_for_symbol
                        and new_coords not in visited
                    ):
                        to_visit_for_symbol.append(new_coords)

                for i in [-1, 1]:
                    new_coords = (curr[0], curr[1] + i)

                    if (
                        new_coords in mapping
                        and mapping[new_coords] == symbol
                        and new_coords not in visited_for_symbol
                        and new_coords not in visited
                    ):
                        to_visit_for_symbol.append(new_coords)

            regions.add((symbol, frozenset(curr_region)))

    for symbol, region in regions:
        area = len(region)

        # How to find sides? Just find the number of corners.
        sides = 0

        for row, col in region:
            for i, j, adj_1, adj_2 in [
                (1, 1, (0, 1), (1, 0)),
                (1, -1, (0, -1), (1, 0)),
                (-1, 1, (0, 1), (-1, 0)),
                (-1, -1, (0, -1), (-1, 0)),
            ]:
                diag = ((row + i), (col + j))
                adj_1 = (row + adj_1[0], col + adj_1[1])
                adj_2 = (row + adj_2[0], col + adj_2[1])

                is_diag_out = diag not in mapping or diag not in region
                is_adj_1_out = adj_1 not in mapping or adj_1 not in region
                is_adj_2_out = adj_2 not in mapping or adj_2 not in region

                sides += bool(
                    (is_diag_out and is_adj_1_out and is_adj_2_out)
                    or (is_diag_out and not is_adj_1_out and not is_adj_2_out)
                    or (not is_diag_out and is_adj_1_out and is_adj_2_out)
                )

        cost = area * sides
        # print(f"{symbol} -> area = {area}, sides = {sides}, cost = {cost}")

        answer += cost

    print(f"Part 2: {answer}")


part_one()
part_two()
