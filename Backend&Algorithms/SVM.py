import pandas as pd
import numpy as np
import joblib
import torch
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from transformers import BertTokenizer, BertModel
from sklearn.model_selection import train_test_split

# Cargar el modelo y el tokenizador BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

# Función para procesar el texto con BERT
def procesar_con_bert(texto: str):
    """
    Convierte el texto en un vector numérico utilizando BERT.
    """
    if pd.isna(texto) or not isinstance(texto, str):  # Manejar valores nulos o no string
        texto = ""
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy().flatten()

# Cargar el archivo CSV
def cargarDatos(rutaArchivo):
    return pd.read_csv(rutaArchivo)

# Preprocesar los datos (convertir columnas categóricas en numéricas y preparar X, y)
def preprocesarDatos(df, columnaObjetivo):
    """
    Convierte las columnas categóricas en numéricas y divide el DataFrame en características (X) y variable objetivo (y).
    """
    # Crear un LabelEncoder para la variable objetivo
    label_encoder = LabelEncoder()  
    df[columnaObjetivo] = label_encoder.fit_transform(df[columnaObjetivo])  # Codificar las categorías

    # Separar las características (X) y la variable objetivo (y)
    X = df.drop(columns=[columnaObjetivo])  # Características (sin la columna objetivo)
    y = df[columnaObjetivo]  # Variable objetivo
    
    return X, y, label_encoder  # Retornar las características, la variable objetivo y el label_encoder

# Cargar los datos
df = cargarDatos(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\archivo_modificado.csv")

# Verificar los nombres exactos de las columnas
df.columns = df.columns.str.strip()
if 'categoria_num' not in df.columns:
    raise ValueError("La columna 'categoria_num' no se encuentra en el DataFrame.")

# Generar los embeddings de BERT para la columna 'categoria_num'
X_bert = np.array([procesar_con_bert(str(concepto)) for concepto in df['categoria_num']])

# Normalizar los embeddings con StandardScaler
scaler = StandardScaler()
X_bert_scaled = scaler.fit_transform(X_bert)

# Preprocesar los datos usando la columna 'categoria_num' como objetivo
X, y, label_encoder = preprocesarDatos(df, 'categoria_num')

# Asegurar que X_bert_scaled e y tienen la misma cantidad de filas
if X_bert_scaled.shape[0] != y.shape[0]:
    raise ValueError(f"Dimensiones no coinciden: X_bert_scaled={X_bert_scaled.shape[0]}, y={y.shape[0]}")

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_bert_scaled, y, test_size=0.2, random_state=42)

# Entrenar el modelo SVM
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Evaluar el modelo SVM en los datos de prueba
y_pred = svm_model.predict(X_test)
accuracy = (y_pred == y_test).mean()
print(f"Precisión del modelo SVM: {accuracy:.2f}")

# Guardar los modelos
joblib.dump(svm_model, 'svm_modelo.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Modelos SVM, scaler y label_encoder guardados correctamente.")
