#!/bin/python3

import os
import sys

import requests

# Script to watch for and pull the input for a given day.

day = sys.argv[1]

with open(f"day_{day.zfill(2)}/input.txt", "a+") as i:
    i.seek(0)
    curr = i.read()
    if len(curr) > 0 and not curr.startswith("Please don't"):
        print("Not writing as input file is populated. Stopping.")
        exit(0)

    session = os.environ["AOC_SESSION"]

    headers = {"Cookie": f"session={session}"}
    response = requests.get(
        f"https://adventofcode.com/2024/day/{day}/input", headers=headers
    )

    input = response.text

    print(f"Writing to day_{day.zfill(2)}/input.txt")
    i.write(input)
