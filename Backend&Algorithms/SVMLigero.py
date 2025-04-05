import pandas as pd
import joblib
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, DistilBertModel
import torch

# Cargar datos
df = pd.read_csv(r"C:\Users\David Ramirez\Documents\CursoSamsunsung2024\Proyecto Final\DB\archivo_modificado.csv")
print("Columnas disponibles en el DataFrame:", df.columns)

# Verificar valores únicos en 'tipo_gasto'
print("Valores únicos en 'tipo_gasto':", df['tipo_gasto'].unique())

# Convertir 'tipo_gasto' a valores numéricos
label_encoder = LabelEncoder()
df['tipo_gasto'] = label_encoder.fit_transform(df['tipo_gasto'])
joblib.dump(label_encoder, "label_encoder.pkl")  # Guardar encoder para futuras predicciones

# Cargar modelo y tokenizer de BERT
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")

def procesar_con_bert(texto):
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

# Procesar categorías con BERT
X_bert = [procesar_con_bert(str(texto)) for texto in df['categoria_num']]
X_bert = torch.tensor(X_bert).squeeze(1).numpy()

# Definir etiquetas
y = df['tipo_gasto']

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_bert, y, test_size=0.2, random_state=42)

# Entrenar modelo SVM
modelo_svm = SVC(kernel='linear')
modelo_svm.fit(X_train, y_train)

# Guardar el modelo entrenado
joblib.dump(modelo_svm, "modelo_svm.pkl")

print("Modelo SVM entrenado y guardado correctamente.")
