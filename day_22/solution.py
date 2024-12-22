#!/bin/python3

import sys
from typing import List


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(int(line))

    return lines


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(secret: int) -> int:
    return secret % 16777216


def evolve(secret: int) -> int:
    step_one = secret * 64
    step_one = mix(step_one, secret)
    step_one = prune(step_one)

    step_two = step_one // 32
    step_two = mix(step_one, step_two)
    step_two = prune(step_two)

    step_three = step_two * 2048
    step_three = mix(step_two, step_three)
    step_three = prune(step_three)

    return step_three


def part_one():
    lines = read_lines_to_list()
    answer = 0

    for line in lines:
        curr = line
        for _i in range(2000):
            curr = evolve(curr)

        answer += curr

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    all_sequences = []
    to_test = set()

    for line in lines:
        prices = []

        curr = line
        for _i in range(2000):
            prices.append(curr % 10)
            curr = evolve(curr)

        deltas = []
        for i in range(len(prices) - 1):
            a = prices[i]
            b = prices[i + 1]
            deltas.append(b - a)

        sequences = dict()
        for i in range(4, len(prices) - 1):
            # Try and take the sequences lining up with this.
            # For index 6, for example, take 2, 3, 4, 5 from delta

            changes = tuple(deltas[i - 4 : i])
            if changes not in sequences:
                sequences[changes] = prices[i]

        to_test.update(sequences.keys())
        all_sequences.append(sequences)

    best_score = 0

    for candidate in to_test:
        total = 0
        for sequence in all_sequences:
            if candidate in sequence:
                total += sequence[candidate]

        if total > best_score:
            best_score = total

    answer = best_score

    print(f"Part 2: {answer}")


part_one()
part_two()
