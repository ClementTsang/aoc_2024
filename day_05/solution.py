#!/bin/python3

import sys
from collections import defaultdict
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(line)

    return lines


def read(lines: List[str]):
    first_section = True
    after_rules = defaultdict(list)
    before_rules = defaultdict(list)
    updates = []
    for line in lines:
        if len(line) == 0:
            first_section = False
            continue

        if first_section:
            [left, right] = line.split("|")
            left = int(left)
            right = int(right)

            after_rules[left].append(right)
            before_rules[right].append(left)
        else:
            update = [int(i) for i in line.split(",")]
            updates.append(update)

    return (updates, after_rules, before_rules)


def valid_update(after_rules, before_rules, update) -> bool:

    for i in range(len(update)):
        before = update[:i]
        after = update[i + 1 :]

        if any(before_rules[b] and update[i] in before_rules[b] for b in before):
            return False

        if any(
            after_rules[update[i]] and a not in after_rules[update[i]] for a in after
        ):
            return False

    return True


def part_one():
    lines = read_lines_to_list()
    answer = 0
    updates, after_rules, before_rules = read(lines)

    for update in updates:
        if valid_update(after_rules, before_rules, update):
            answer += update[len(update) // 2]

    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0
    updates, after_rules, before_rules = read(lines)

    for update in updates:
        if not valid_update(after_rules, before_rules, update):
            # Lazy way of doing it: just brute force shuffle values until it's sorted.
            # Not the most clean but it _does_ seem to work...
            new_update = []
            while update:
                curr = update.pop(0)
                if all(u in after_rules[curr] for u in update):
                    new_update.append(curr)
                else:
                    update.append(curr)

            answer += new_update[len(new_update) // 2]

    print(f"Part 2: {answer}")


part_one()
part_two()
