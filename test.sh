#!/bin/bash

set -e

DAY="day_$(printf '%02d' "$1")"
FILE="${2:-test.txt}"

echo "===== Running TEST for $DAY on file $FILE ====="

source .venv_normal/bin/activate
.venv/bin/python "$DAY/solution.py" "$DAY/$FILE" $3