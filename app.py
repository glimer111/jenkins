from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


MODEL_PATH = Path("models/cars_price_model.pkl")


class CarFeatures(BaseModel):
    Make: str
    Model: str
    Year: int
    Style: str
    Distance: float
    Engine_capacity_cm3: float
    Fuel_type: str
    Transmission: str


app = FastAPI(title="Cars Price Model Service")


def load_model():
    return joblib.load(MODEL_PATH)


@app.get("/health")
def health() -> dict[str, str]:
    if not MODEL_PATH.exists():
        return {"status": "model_not_found"}
    return {"status": "ok"}


@app.post("/predict")
def predict(car: CarFeatures) -> dict[str, float]:
    model = load_model()
    row = {
        "Make": car.Make,
        "Model": car.Model,
        "Year": car.Year,
        "Style": car.Style,
        "Distance": car.Distance,
        "Engine_capacity(cm3)": car.Engine_capacity_cm3,
        "Fuel_type": car.Fuel_type,
        "Transmission": car.Transmission,
    }
    prediction = model.predict(pd.DataFrame([row]))[0]
    return {"predicted_price_euro": round(float(prediction), 2)}
