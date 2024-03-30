from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
import spacy

app = FastAPI()
# para correr front yarn dev
# para correr back uvicorn main:app --reload

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Text(BaseModel):
    text: str

# Cargar palabras abstractas desde un archivo XLSX
def cargar_palabras_abstractas(archivo):
    abstract_dict = {}
    data_xlsx = pd.read_excel(archivo, usecols=[0, 1, 2])
    for row in data_xlsx.itertuples(index=False):
        palabra = str(row[0]).lower()
        es_compuesta = row[1]
        concreteness = row[2]
        if concreteness <= 3.9:
            abstract_dict[palabra] = (es_compuesta, concreteness)
    return abstract_dict

# Función para detectar lenguaje abstracto usando SpaCy

nlp = spacy.load("en_core_web_trf")
def detect_abstract_language_spacy(text):
    abstract_terms = []
    doc = nlp(text)
    lista =[]
    for token in doc:
        lista.append((token, token.pos_))
        # Excluir de la frase preposiciones, pronombres posesivos, pronombres personales, determinantes, conjunciones coordinantes,verbos particulares, conjunciones subordinantes, y verbos en presente 3ra persona singular
        if token.pos_ not in ["PRON", "DET", "CCONJ", "ADP", "PART", "SCONJ"] and not (token.pos_ == "VERB" and token.tag_ == "VBZ"):
            abstract_terms.append(token.text.lower())
    print(lista)
    print("\n")
    return abstract_terms


@app.on_event("startup")
async def startup_event():
    global abstractWords, ZviAbstractWords

    # Cargar palabras abstractas
    listOfWords40000 = './xlsx/LIST WORDS FROM Concreteness ratings for 40 thousand generally known English word lemmas.xlsx'
    listOfWordsZvi = './xlsx/Abstract_Zvi_List.xlsx'
    abstractWords = cargar_palabras_abstractas(listOfWords40000)
    ZviAbstractWords = cargar_palabras_abstractas(listOfWordsZvi)
    abstractWords.update(ZviAbstractWords)


@app.post("/detect")
async def detect_abstract_words(item: Text):

    # Detectar palabras abstractas
    inputWords = set(detect_abstract_language_spacy(item.text))
    palabras_abstractas_encontradas = inputWords.intersection(abstractWords)

    # Agregar palabras abstractas compuestas presentes
    for word, (es_compuesta, _) in abstractWords.items():
        if (es_compuesta == 1) and (word in item.text) and (word not in palabras_abstractas_encontradas):
            palabras_abstractas_encontradas.add(word)

    return {"abstractWords": list(palabras_abstractas_encontradas)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
