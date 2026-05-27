from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_URL = (
    "https://raw.githubusercontent.com/dayekb/Basic_ML_Alg/main/"
    "cars_moldova_no_dup.csv"
)
RAW_DIR = Path("data/raw")
RAW_PATH = RAW_DIR / "cars_raw.csv"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_URL)
    df.to_csv(RAW_PATH, index=False)
    print(f"Downloaded {len(df)} rows to {RAW_PATH}")


if __name__ == "__main__":
    main()
