#!/bin/bash

set -eu

DAY="day_$(printf '%02d' "$1")"

echo "===== Running SOLVE for $DAY ====="

source .venv/bin/activate
.venv/bin/python "$DAY/solution.py" "$DAY/input.txt"