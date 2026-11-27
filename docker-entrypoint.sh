#!/bin/sh
set -e
if [ ! -d /app/mlruns ] || [ -z "$(ls -A /app/mlruns)" ]; then
  python train.py
fi
exec uvicorn main:app --host 0.0.0.0 --port 8000
