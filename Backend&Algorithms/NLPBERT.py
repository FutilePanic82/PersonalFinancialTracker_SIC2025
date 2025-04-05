import re
import spacy
import unicodedata
from sentence_transformers import SentenceTransformer

# Cargamos el modelo de lenguaje de spaCy y el modelo para BERT
nlp = spacy.load("es_core_news_md") 
bert_model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

def normalizar_texto(textoANormalizar):
    # Convertir a minúsculas
    textoANormalizar = textoANormalizar.lower()
    # Eliminar acentos
    textoANormalizar = unicodedata.normalize('NFKD', textoANormalizar).encode('ASCII', 'ignore').decode('utf-8')
    
    return textoANormalizar

def preprocess(texto):
    listaTokens = []
    listaLemma = []

    doc = nlp(texto)

    #Obtener monto
    match = re.search(r'(\$?\d+(?:[.,]\d+)?)', texto)
    monto = None
    if match:
        monto = float(match.group(1).replace("$", "").replace(",", ""))
        print("Monto detectado:", monto)
    else:
        print("No se detectó monto.")

    #Tokenización 
    for x in doc:
        listaTokens.append(x.text)
    print("Tokenizacion: ", listaTokens)

    #Lematización de cada palabra tokenizada
    for token in doc:
        #Filtro para las palabras de parada y puntiaciones
        if not token.is_stop and not token.is_punct:
            listaLemma.append(token.lemma_)
    print("Lematizacion: ", listaLemma)

    #Obtener entidades
    for ent in doc.ents:
        print("entidades detectadas: ", ent.text, "->", ent.label_)
    
    # Generar vector semántico BERT
    texto_para_embedding = " ".join(texto) #se está utilizando el texto normalizado

    vector_bert = bert_model.encode(texto_para_embedding)

    print("Vector BERT:", vector_bert)


def main():
    textoUsuario = "Gasté $1000 pesos en un iphone de apple, muy caro, tambien compre unos audifonos earpods en 3299 pesos"
    textoNormalizado = normalizar_texto(textoUsuario)
    preprocess(textoNormalizado)

if __name__ == "__main__":
    main()