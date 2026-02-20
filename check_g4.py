
import pandas as pd
import os

try:
    df = pd.read_csv("DataBase/archivo_modificado.csv")
    print("Unique values in tipo_gasto:")
    print(df['tipo_gasto'].unique())
    print("\nValue counts:")
    print(df['tipo_gasto'].value_counts())
except Exception as e:
    print(f"Error: {e}")
