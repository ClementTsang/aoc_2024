#!/bin/bash

set -e

DAY="day_$(printf '%02d' "$1")"

echo "===== Running SOLVE for $DAY using pypy ====="

source .venv/bin/activate
# .venv/bin/python "$DAY/solution.py" "$DAY/input.txt" $2
pypy3 "$DAY/solution.py" "$DAY/input.txt" $2

