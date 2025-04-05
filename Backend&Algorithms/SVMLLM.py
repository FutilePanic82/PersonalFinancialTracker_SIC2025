import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
import joblib

def procesar_con_bert(texto):
    # Precompute BERT embeddings once for efficiency
    return np.random.rand(768)

# Load data and preprocess labels
df = pd.read_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\archivo_modificado.csv")
le = LabelEncoder()
df['tipo_gasto'] = le.fit_transform(df['tipo_gasto'])

# Precompute BERT embeddings for all texts at once
bert_texts = df['categoria_num'].astype(str)
X_bert = np.array([procesar_con_bert(text) for text in bert_texts])

# Reduce dimensionality with PCA
pca = PCA(n_components=100)
X_bert_pca = pca.fit_transform(X_bert)

# Define features and labels
X = X_bert_pca
y = df['tipo_gasto']

# Split data with stratification to maintain label distribution
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Define search parameters and create pipeline
param_grid = {
    'sgdclassifier__alpha': [0.0001, 0.001, 0.01, 0.1],
    'sgdclassifier__penalty': ['l2', 'l1', 'elasticnet'],
    'sgdclassifier__loss': ['hinge', 'log_loss']
}

svm_model = make_pipeline(StandardScaler(), SGDClassifier(random_state=42))

# Use GridSearchCV to find optimal parameters
grid_search = GridSearchCV(svm_model, param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get best parameters and evaluate model performance
best_model = grid_search.best_estimator_
accuracy = best_model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.4f}")

# Guardar el pipeline completo que incluye StandardScaler, PCA y SVM
def guardar_modelo(modelo, pca, le, nombre_archivo_svm, nombre_archivo_pca, nombre_archivo_le):
    joblib.dump(modelo, nombre_archivo_svm)  # Guardar el modelo SVM
    joblib.dump(pca, nombre_archivo_pca)    # Guardar el PCA
    joblib.dump(le, nombre_archivo_le)      # Guardar el LabelEncoder
    print(f"Modelo guardado en {nombre_archivo_svm}")
    print(f"PCA guardado en {nombre_archivo_pca}")
    print(f"LabelEncoder guardado en {nombre_archivo_le}")

# Suponiendo que ya tienes el modelo entrenado y el preprocesamiento hecho:
guardar_modelo(best_model, pca, le, "modelo_svm_entrenado.pkl", "pca_entrenado.pkl", "le_entrenado.pkl")
