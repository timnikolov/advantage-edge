#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " AdVantage-Edge: Contextual Intent Arbiter & Monetization"
echo "=========================================================="
echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

export PYTHONPATH="$DIR:$PYTHONPATH"

echo "[1/4] Initializing SQLite Catalog Database (100+ Products)..."
python3 data/init_db.py

echo ""
echo "[2/4] Verifying Evaluation Dataset (150 Synthetic Test Cases)..."
python3 data/generate_dataset.py

echo ""
echo "[3/4] Running Pytest Unit Test Suite..."
python3 -m pytest tests/ -v

echo ""
echo "[4/4] Executing Offline Benchmark & Evaluation Defense Suite..."
python3 eval/run_eval.py

echo ""
echo "=========================================================="
echo " AdVantage-Edge Execution Complete! All SLAs Verified."
echo "=========================================================="
