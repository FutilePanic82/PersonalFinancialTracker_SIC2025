import pandas as pd
import os

# Cargamos el dataset
df =  pd.read_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\GASTOS.csv", encoding="ISO-8859-1")

# Definimos un diccionario para las categorías generales
categorias = {
    1: "Alimentos",
    2: "Transporte", 
    3: "Vivienda",
    4: "Cuidado personal",
    5: "Educación y recreación",
    6: "Comunicaciones",
    7: "Vestimenta",
    8: "Salud",
    9: "Artículos domésticos",
    10: "Gastos diversos"
}

# Función para asignar categoría según el código de gasto
def asignar_categoria(codigo):
    prefix = codigo[0]
    num = int(codigo[1:]) if codigo[1:].isdigit() else 0
    
    # Alimentos (A001-A242)
    if prefix == 'A':
        return 1
    
    # Transporte (B001-B007, M001-M018)
    elif prefix == 'B' or prefix == 'M':
        return 2
    
    # Vivienda (G001-G016, G101-G106, R001-R013, K040-K045)
    elif prefix == 'G' or prefix == 'R' or (prefix == 'K' and num >= 40 and num <= 45):
        return 3
    
    # Cuidado personal (D001-D026, C001-C024)
    elif prefix == 'D' or prefix == 'C':
        return 4
    
    # Educación y recreación (E001-E034, L001-L029)
    elif prefix == 'E' or prefix == 'L':
        return 5
    
    # Comunicaciones (F001-F014)
    elif prefix == 'F':
        return 6
    
    # Vestimenta (H001-H136)
    elif prefix == 'H':
        return 7
    
    # Salud (J001-J072)
    elif prefix == 'J':
        return 8
    
    # Artículos domésticos (I001-I026, K001-K039)
    elif prefix == 'I' or (prefix == 'K' and num < 40):
        return 9
    
    # Gastos diversos (N001-N016, T901-T916)
    elif prefix == 'N' or prefix == 'T':
        return 10
    
    # En caso de que no encaje en las categorías anteriores
    else:
        return 0

# Aplicamos la función para crear la nueva columna
df['categoria_num'] = df['gastos'].apply(asignar_categoria)

# Agregamos la descripción de la categoría
df['categoria_desc'] = df['categoria_num'].map(categorias)

# Guardamos el resultado en un nuevo CSV
df.to_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\GASTOS_CLASIFICADOS2.csv", index=False)

# Mostrar las primeras filas
print(df.head())

# Mostrar la distribución de categorías
print(df['categoria_desc'].value_counts())