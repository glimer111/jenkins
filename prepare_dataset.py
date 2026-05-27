from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


RAW_PATH = Path("data/raw/cars_raw.csv")
PROCESSED_DIR = Path("data/processed")
CLEAN_PATH = PROCESSED_DIR / "cars_clean.csv"
TRAIN_PATH = PROCESSED_DIR / "train.csv"
TEST_PATH = PROCESSED_DIR / "test.csv"
TARGET = "Price(euro)"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().dropna()

    df = df.drop(df[(df.Year < 2021) & (df.Distance < 1100)].index)
    df = df.drop(df[df.Distance > 1e6].index)
    df = df.drop(df[df["Engine_capacity(cm3)"] < 200].index)
    df = df.drop(df[df["Engine_capacity(cm3)"] > 5000].index)
    df = df.drop(df[df[TARGET] < 101].index)
    df = df.drop(df[df[TARGET] > 1e5].index)
    df = df.drop(df[df.Year < 1971].index)

    feature_columns = [
        "Make",
        "Model",
        "Year",
        "Style",
        "Distance",
        "Engine_capacity(cm3)",
        "Fuel_type",
        "Transmission",
        TARGET,
    ]
    return df[feature_columns].reset_index(drop=True)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW_PATH)
    clean = clean_data(df)

    train_df, test_df = train_test_split(
        clean,
        test_size=0.3,
        random_state=42,
    )

    clean.to_csv(CLEAN_PATH, index=False)
    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)

    print(f"Clean rows: {len(clean)}")
    print(f"Train rows: {len(train_df)} -> {TRAIN_PATH}")
    print(f"Test rows: {len(test_df)} -> {TEST_PATH}")


if __name__ == "__main__":
    main()
