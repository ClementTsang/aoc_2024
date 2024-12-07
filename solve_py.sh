#!/bin/bash

set -e

DAY="day_$(printf '%02d' "$1")"

echo "===== Running SOLVE for $DAY using python ====="

source .venv_normal/bin/activate
.venv/bin/python "$DAY/solution.py" "$DAY/input.txt" $2

