"""
RegresionPolinomica.py — Script de prueba/entrenamiento del modelo predictivo (Referencia).
Usa regresión lineal polinómica de grado 2.
"""
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def main():
    # ── Rutas ──────────────────────────────────────────────────────────────────
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_DIR = os.path.join(BASE_DIR, "..", "DataBase")
    CSV_PATH = os.path.join(DB_DIR, "dataset_gestor_gastos.csv")
    
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encontró el dataset en {CSV_PATH}")
        return

    # 1. Cargar el dataset
    print(f"Cargando dataset desde {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    # 2. Seleccionar variables independientes (X) y variable dependiente (y)
    X = df[['Ingresos', 'Hijos', 'Edad', 'Educacion']]
    y = df['Gasto']

    # 3. Dividir en entrenamiento y prueba (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Transformar las variables con características polinomiales (grado 2)
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # 5. Entrenar el modelo de regresión lineal sobre los datos polinomiales
    model = LinearRegression()
    model.fit(X_train_poly, y_train)

    # 6. Realizar predicciones
    y_pred = model.predict(X_test_poly)

    # 7. Evaluar el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("📊 Evaluación del Modelo Polinomial (grado 2):")
    print(f"🔹 Error Cuadrático Medio (MSE): {mse:.2f}")
    print(f"🔹 Coeficiente de Determinación (R²): {r2:.4f}")

    # 8. Ver coeficientes
    feature_names = poly.get_feature_names_out(X.columns)
    coef_df = pd.DataFrame({
        'Variable': feature_names,
        'Coeficiente': model.coef_
    })
    print("\n🔍 Coeficientes del modelo:")
    print(coef_df)

if __name__ == "__main__":
    main()
