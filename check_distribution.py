
import pandas as pd

try:
    df = pd.read_csv("DataBase/archivo_modificado.csv")
    print("Class distribution in tipo_gasto:")
    print(df['tipo_gasto'].value_counts())
    print("\nUnique values:", df['tipo_gasto'].unique())
except Exception as e:
    print(f"Error: {e}")
