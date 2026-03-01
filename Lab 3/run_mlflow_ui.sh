#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Use a sqlite backend and keep artifacts under ./mlruns.
mlflow ui \
  --backend-store-uri "sqlite:///mlflow.db" \
  --default-artifact-root "./mlruns" \
  --host 127.0.0.1 \
  --port 5001
