import pandas as pd
import os

# Cargar los archivos CSV
df_diccionario = pd.read_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\GASTOS.csv", encoding="ISO-8859-1")
df_original = pd.read_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\ConjuntoDatos.csv", encoding="ISO-8859-1")

# Mostrar nombres de columnas
print("Columnas en df_original:", df_original.columns)
print("Columnas en df_diccionario:", df_diccionario.columns)

# Eliminar espacios en los nombres de columnas
df_diccionario.columns = df_diccionario.columns.str.strip()
df_original.columns = df_original.columns.str.strip()

# Renombrar la columna 'gastos' en df_diccionario para que coincida con df_original
df_diccionario.rename(columns={"gastos": "tipo_gasto"}, inplace=True)

# Realizar la unión usando 'tipo_gasto'
df_merged = df_original.merge(df_diccionario, on="tipo_gasto", how="left")

# Guardar el archivo con la nueva clasificación
df_merged.to_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\DATOS_CLASIFICADOS.csv", index=False, encoding="ISO-8859-1")

print("Clasificación agregada correctamente y guardada en 'DATOS_CLASIFICADOS.csv'.")