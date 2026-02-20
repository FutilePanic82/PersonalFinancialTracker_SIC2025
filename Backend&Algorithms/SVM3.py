"""
SVM3.py — Script de re-entrenamiento del modelo de clasificación (Referencia).
Usa DistilBERT embeddings + SVM para clasificar conceptos de gasto.
"""
import os
import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, DistilBertModel
from tqdm import tqdm

# ── Configuración de Rutas ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "DataBase")
CSV_PATH = os.path.join(DB_DIR, "GASTOS_CLASIFICADOS2.csv") # Usar el dataset con mejores categorías

# ── Configuración de Device ────────────────────────────────────────────────────
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando dispositivo: {DEVICE}")

def main():
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encontró el dataset en {CSV_PATH}")
        return

    print("Cargando dataset...")
    df = pd.read_csv(CSV_PATH)

    # Filtrar posibles filas con valores nulos en columnas críticas
    df = df.dropna(subset=['descripcion', 'categoria_desc'])
    
    # Filtrar etiquetas ruidosas (como números o "etcétera")
    # Nos quedamos solo con las categorías principales que detectamos antes
    valid_categories = [
        'Alimentos', 'Artículos domésticos', 'Comunicaciones', 
        'Cuidado personal', 'Educación y recreación', 'Gastos diversos', 
        'Salud', 'Transporte', 'Vestimenta', 'Vivienda'
    ]
    df = df[df['categoria_desc'].isin(valid_categories)]

    print(f"Dataset cargado y filtrado: {len(df)} registros para entrenamiento.")

    # Codificar la columna de categorías
    le = LabelEncoder()
    df['tipo_gasto'] = le.fit_transform(df['categoria_desc'])

    # Cargar modelo BERT
    print("Cargando DistilBERT...")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model_bert = DistilBertModel.from_pretrained('distilbert-base-uncased').to(DEVICE)

    def procesar_con_bert(texto):
        if not isinstance(texto, str):
            texto = str(texto)
        inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True, max_length=128).to(DEVICE)
        with torch.no_grad():
            outputs = model_bert(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()

    # Generar embeddings de BERT
    print("Generando embeddings...")
    tqdm.pandas()
    df['bert_embedding'] = df['descripcion'].astype(str).progress_apply(procesar_con_bert)

    # Convertir embeddings a matriz
    X_bert = np.vstack(df['bert_embedding'].values)

    # Reducir dimensionalidad con PCA
    print("Reduciendo dimensionalidad con PCA...")
    pca = PCA(n_components=50)
    X_bert_pca = pca.fit_transform(X_bert)

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X_bert_pca, df['tipo_gasto'], test_size=0.2, random_state=42, stratify=df['tipo_gasto']
    )

    # Entrenar SVM con kernel RBF
    print("Entrenando Svm...")
    svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
    svm_model.fit(X_train, y_train)

    score = svm_model.score(X_test, y_test)
    print(f"✅ Modelo entrenado. Precisión en test: {score:.4f}")

    # Guardar modelos
    print("Guardando modelos .pkl...")
    joblib.dump(svm_model, os.path.join(BASE_DIR, 'modelo_svm_entrenado.pkl'))
    joblib.dump(pca, os.path.join(BASE_DIR, 'pca_entrenado.pkl'))
    joblib.dump(le, os.path.join(BASE_DIR, 'le_entrenado.pkl'))
    print("¡Listo!")

if __name__ == "__main__":
    main()
