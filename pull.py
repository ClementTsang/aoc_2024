#!/bin/python3

import sys

import requests

# Script to watch for and pull the input for a given day.

day = sys.argv[1]

with open(".session") as f, open(f"day_{day.zfill(2)}/input.txt", "r+") as i:
    if len(i.read()) > 0:
        print("Not writing as input file is populated. Stopping.")
        exit(0)

    session = f.read()

    headers = {"Cookie": f"session={session}"}
    response = requests.get(
        f"https://adventofcode.com/2024/day/{day}/input", headers=headers
    )

    input = response.text

    print(f"Writing to day_{day.zfill(2)}/input.txt")
    i.write(input)
