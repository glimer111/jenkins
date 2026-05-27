#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python download_data.py
python prepare_dataset.py
python train_model.py

pkill -f "uvicorn app:app" || true
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > service.log 2>&1 &
sleep 8
python test_service.py
