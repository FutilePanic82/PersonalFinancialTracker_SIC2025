"""
predictor.py — Polynomial-Regression (degree-2) predictor for monthly spending.

Trained automatically at startup from DataBase/dataset_gestor_gastos.csv.
Features: Ingresos, Hijos, Edad, Educacion  →  Gasto
"""
from __future__ import annotations

import logging
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

logger = logging.getLogger(__name__)

# ── Path to training data ───────────────────────────────────────────────────────
BASE     = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE, "..", "DataBase", "dataset_gestor_gastos.csv")

_poly  : PolynomialFeatures | None = None
_model : LinearRegression   | None = None
_r2    : float = 0.0


def _train():
    global _poly, _model, _r2
    logger.info("Training polynomial regression …")
    df = pd.read_csv(CSV_PATH)
    X  = df[["Ingresos", "Hijos", "Edad", "Educacion"]]
    y  = df["Gasto"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    _poly  = PolynomialFeatures(degree=2, include_bias=False)
    X_tr_p = _poly.fit_transform(X_train)
    X_te_p = _poly.transform(X_test)
    _model = LinearRegression()
    _model.fit(X_tr_p, y_train)
    _r2 = round(r2_score(y_test, _model.predict(X_te_p)), 4)
    logger.info("Polynomial regression trained — R²=%.4f ✓", _r2)


# Train once at import-time
_train()


def predecir(ingresos: float, hijos: int, edad: int, educacion: int) -> dict:
    """
    Return predicted monthly spending and the model R² score.

    Parameters
    ----------
    ingresos  : Monthly income
    hijos     : Number of children
    edad      : Age
    educacion : Education level (0=primary … 3=postgraduate)
    """
    if _poly is None or _model is None:
        raise RuntimeError("Model not trained yet")
    X_new  = np.array([[ingresos, hijos, edad, educacion]])
    X_poly = _poly.transform(X_new)
    gasto  = float(_model.predict(X_poly)[0])
    return {
        "gasto_predicho": round(max(gasto, 0), 2),
        "r2": _r2,
        "ahorro_estimado": round(max(ingresos - gasto, 0), 2),
    }
