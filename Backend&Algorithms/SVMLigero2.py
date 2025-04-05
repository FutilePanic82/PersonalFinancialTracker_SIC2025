import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
import joblib
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from concurrent.futures import ProcessPoolExecutor  # Para paralelización en CPU
from tqdm import tqdm  # Para la barra de progreso

# Cargar el archivo CSV con los datos
df = pd.read_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\archivo_modificado.csv")

# Seleccionar solo el 10% de los datos aleatoriamente
df = df.sample(frac=0.1, random_state=42)  

# Preprocesar los datos
le = LabelEncoder()
df['tipo_gasto'] = le.fit_transform(df['tipo_gasto'])

# Cargar modelo BERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model_bert = DistilBertModel.from_pretrained('distilbert-base-uncased')

# Función para obtener embeddings de BERT
def procesar_con_bert(texto):
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model_bert(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# Obtener embeddings usando paralelización
def procesar_todos_los_textos(textos):
    with ProcessPoolExecutor() as executor:
        embeddings = list(tqdm(executor.map(procesar_con_bert, textos), total=len(textos), desc="Procesando BERT", ncols=100))
    return np.array(embeddings)

# Procesar los textos con BERT
if __name__ == '__main__':
    X_bert = procesar_todos_los_textos(df['categoria_num'].astype(str))

    # Reducir dimensionalidad con PCA
    pca = PCA(n_components=50)
    X_bert_pca = pca.fit_transform(X_bert)

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X_bert_pca, df['tipo_gasto'], test_size=0.2, random_state=42, stratify=df['tipo_gasto']
    )

    # Modelo SVM con optimización
    svm_model = make_pipeline(StandardScaler(), SGDClassifier(loss='hinge', max_iter=5000, tol=1e-3, n_jobs=-1))

    # Entrenar con barra de progreso
    for i in tqdm(range(1), desc="Entrenando SVM", ncols=100):
        svm_model.fit(X_train, y_train)

    # Evaluación
    accuracy = svm_model.score(X_test, y_test)
    print(f"Accuracy: {accuracy:.4f}")

    # Guardar el modelo
    joblib.dump(svm_model, 'modelo_svm_entrenado.pkl')
    joblib.dump(pca, 'pca_entrenado.pkl')
    joblib.dump(le, 'le_entrenado.pkl')

    # Función para clasificar un concepto
    def clasificar_concepto(concepto):
        embedding = procesar_con_bert(concepto)
        embedding_pca = pca.transform([embedding])
        prediccion = svm_model.predict(embedding_pca)
        return le.inverse_transform(prediccion)[0]

    # Ejemplo de uso
    print(f"Categoría predicha: {clasificar_concepto('gasto en supermercado')}")
