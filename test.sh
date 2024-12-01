#!/bin/bash

set -eu

DAY="day_$(printf '%02d' "$1")"

echo "===== Running TEST for $DAY ====="

source .venv/bin/activate
.venv/bin/python "$DAY/solution.py" "$DAY/test.txt"