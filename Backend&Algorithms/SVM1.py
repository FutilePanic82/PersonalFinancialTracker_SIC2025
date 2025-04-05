import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score

def cargarDatos(rutaArchivo):
    """
    Carga un archivo CSV en un DataFrame de Pandas.
    :param rutaArchivo: Ruta del archivo CSV.
    :return: DataFrame con los datos cargados.
    """
    return pd.read_csv(rutaArchivo)

def preprocesarDatos(df, columnaObjetivo):
    """
    Separa las características y la variable objetivo, y normaliza los datos.
    Transforma las columnas categóricas a valores numéricos.
    :param df: DataFrame con los datos.
    :param columnaObjetivo: Nombre de la columna objetivo.
    :return: Datos de entrenamiento y prueba.
    """
    # Identificar y transformar las columnas categóricas en numéricas
    label_encoder = LabelEncoder()
    
    # Convertir todas las columnas no numéricas en numéricas
    for columna in df.select_dtypes(include=['object']).columns:
        df[columna] = label_encoder.fit_transform(df[columna])
    
    # Separar las características y la variable objetivo
    X = df.drop(columns=[columnaObjetivo])  # Características
    y = df[columnaObjetivo]  # Variable objetivo
    
    # Eliminar filas con NaN en la variable objetivo
    df = df.dropna(subset=[columnaObjetivo])
    X = df.drop(columns=[columnaObjetivo])
    y = df[columnaObjetivo]
    
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalizar los datos
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test

def entrenarModelo(X_train, y_train):
    """
    Entrena un modelo de SVM con los datos de entrenamiento.
    :param X_train: Características de entrenamiento.
    :param y_train: Etiquetas de entrenamiento.
    :return: Modelo SVM entrenado.
    """
    modelo = SVC(kernel='linear')
    modelo.fit(X_train, y_train)
    return modelo

def evaluarModelo(modelo, X_test, y_test):
    """
    Evalúa el modelo entrenado con datos de prueba y devuelve la precisión.
    :param modelo: Modelo SVM entrenado.
    :param X_test: Características de prueba.
    :param y_test: Etiquetas de prueba.
    :return: Precisión del modelo.
    """
    y_pred = modelo.predict(X_test)
    return accuracy_score(y_test, y_pred)

# Uso del clasificador
df = cargarDatos(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\archivo_modificado.csv")  # Ruta del archivo
X_train, X_test, y_train, y_test = preprocesarDatos(df, 'categoria_num')  # 'categoria_num' es la variable objetivo
modelo = entrenarModelo(X_train, y_train)
precision = evaluarModelo(modelo, X_test, y_test)

print(f'Precisión del modelo: {precision:.2f}')
