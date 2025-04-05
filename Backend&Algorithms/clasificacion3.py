import pandas as pd
import os
def modificar_csv(input_file, output_file, diccionario_file):
    # Cargar el archivo CSV con los datos a modificar
    df = pd.read_csv(input_file, encoding="ISO-8859-1")
    
    # Cargar el archivo CSV como diccionario
    df_dict = pd.read_csv(diccionario_file, encoding="ISO-8859-1")
    dict_gastos = dict(zip(df_dict['gastos'], df_dict['categoria_num']))
    
    # Agregar la columna 'categoria_num' al archivo a modificar
    df['categoria_num'] = df['gastos'].map(dict_gastos)
    
    # Guardar el archivo modificado
    df.to_csv(output_file, index=False)
    print(f"Archivo modificado guardado en: {output_file}")

# Rutas de archivos
input_file = r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\ConjuntoDatos.csv"
diccionario_file = r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\GASTOS_CLASIFICADOS2.csv"
output_file = r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\archivo_modificado.csv"

# Llamar a la función
modificar_csv(input_file, output_file, diccionario_file)
