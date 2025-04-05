import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.svm import SVC
import joblib
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from tqdm import tqdm

# Cargar el archivo CSV
df = pd.read_csv("C:/Users/David Ramirez/Documents/CursoSamsunsung2024/Proyecto Final/DB/archivo_modificado.csv")

# Tomar solo una muestra del 10% de los datos
df = df.sample(frac=0.1, random_state=42)

# Codificar la columna de categorías
le = LabelEncoder()
df['tipo_gasto'] = le.fit_transform(df['tipo_gasto'])

# Cargar modelo BERT
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model_bert = DistilBertModel.from_pretrained('distilbert-base-uncased').to(device)

def procesar_con_bert(texto):
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model_bert(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()

# Generar embeddings de BERT
tqdm.pandas()
df['bert_embedding'] = df['categoria_num'].astype(str).progress_apply(procesar_con_bert)

# Convertir embeddings a matriz
X_bert = np.vstack(df['bert_embedding'].values)

# Reducir dimensionalidad con PCA
pca = PCA(n_components=50)
X_bert_pca = pca.fit_transform(X_bert)

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X_bert_pca, df['tipo_gasto'], test_size=0.2, random_state=42, stratify=df['tipo_gasto']
)

# Entrenar SVM con kernel RBF
svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
svm_model.fit(X_train, y_train)

# Guardar modelos
joblib.dump(svm_model, 'modelo_svm_entrenado.pkl')
joblib.dump(pca, 'pca_entrenado.pkl')
joblib.dump(le, 'le_entrenado.pkl')

def clasificar_concepto(concepto):
    embedding = procesar_con_bert(concepto)
    embedding_pca = pca.transform([embedding])
    prediccion = svm_model.predict(embedding_pca)
    return le.inverse_transform(prediccion)[0]

# Ejemplo
ejemplo = "gasto en supermercado"
print(f"Categoría predicha: {clasificar_concepto(ejemplo)}")
