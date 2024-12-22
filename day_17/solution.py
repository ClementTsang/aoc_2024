#!/bin/python3

import sys
from typing import List

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def read_lines_to_list() -> List[str]:
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lines.append(line)

    return lines


def combo(register_a, register_b, register_c, operand) -> int:
    if operand in [0, 1, 2, 3]:
        combo = operand
    elif operand == 4:
        combo = register_a
    elif operand == 5:
        combo = register_b
    elif operand == 6:
        combo = register_c
    elif operand == 7:
        raise Exception("this is a reserved combo operand")
    else:
        raise Exception("you messed up")

    return combo


def part_one():
    lines = read_lines_to_list()
    answer = ""

    register_a = int(lines[0].split(": ")[-1])
    register_b = int(lines[1].split(": ")[-1])
    register_c = int(lines[2].split(": ")[-1])
    program = [int(v) for v in lines[4].split(": ")[-1].split(",")]

    pc = 0
    out = []
    while pc < len(program):
        opcode = program[pc]
        operand = program[pc + 1]
        combo_operand = combo(register_a, register_b, register_c, operand)

        if opcode == 0:
            # adv
            register_a = register_a // pow(2, combo_operand)
        elif opcode == 1:
            # bxl
            register_b = register_b ^ operand
        elif opcode == 2:
            # bst
            register_b = combo_operand % 8
        elif opcode == 3:
            # jnz
            if register_a != 0:
                pc = operand
                continue
        elif opcode == 4:
            # bxc
            register_b = register_b ^ register_c
        elif opcode == 5:
            # out
            out.append(f"{combo_operand % 8}")
        elif opcode == 6:
            # bdv
            register_b = register_a // pow(2, combo_operand)
        elif opcode == 7:
            # cdv
            register_c = register_a // pow(2, combo_operand)
        else:
            raise Exception("non-existent opcode!")

        pc += 2

    answer = ",".join(out)
    print(f"Part 1: {answer}")


def part_two():
    lines = read_lines_to_list()
    answer = 0

    program = [int(v) for v in lines[4].split(": ")[-1].split(",")]

    def test(a):
        return (((a % 8) ^ 1) ^ 5) ^ (a // pow(2, ((a % 8) ^ 1))) % 8

    answers = [0]
    for p in reversed(program):
        new_answers = []
        for curr in answers:
            for a in range(8):
                to_test = (curr << 3) + a
                out = test(to_test)
                if out == p:
                    new_answers.append(to_test)

        answers = new_answers

    answer = min(answers)

    print(f"Part 2: {answer}")


part_one()
part_two()
