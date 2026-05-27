from __future__ import annotations

import json
from pathlib import Path

import requests


SERVICE_URL = "http://127.0.0.1:8000/predict"
REQUEST_PATH = Path("sample_request.json")


def main() -> None:
    payload = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    response = requests.post(SERVICE_URL, json=payload, timeout=20)
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
