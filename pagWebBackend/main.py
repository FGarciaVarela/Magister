import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
import nltk

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


app = FastAPI()

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
    concrete_dict = {}
    abstract_dict = {}
    data_xlsx = pd.read_excel(archivo, usecols=[0, 1, 2])
    for row in data_xlsx.itertuples(index=False):
        palabra = str(row[0]).lower()
        es_compuesta = row[1]
        concreteness = row[2]
        if concreteness <= 3.9:
            abstract_dict[palabra] = (es_compuesta, concreteness)
        if concreteness > 3.9:
            concrete_dict[palabra] = (es_compuesta, concreteness)
    return abstract_dict, concrete_dict

# Función para detectar lenguaje abstracto usando SpaCy

def detect_abstract_language_nltk(text):
    stop_words = set(stopwords.words('english'))

    abstract_terms = []
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)

    # print("Lista de tokens y sus etiquetas POS:")
    # for token, tag in tagged_tokens:
    #     print((token, tag))
    
       # Excluir de la frase preposiciones, pronombres posesivos, pronombres personales, determinantes, conjunciones coordinantes,verbos particulares, conjunciones subordinantes, verbos en presente 3ra persona singular
    excluded_tags = ["PRP",'PRP$' , "DT", "CC", "IN", "POS", "TO", "WDT", "WP", "WP$", "WRB"]
    for token, tag in tagged_tokens:
        # Excluir basado en etiquetas POS; VBZ no se maneja directamente aquí, necesita ser revisado específicamente
        if tag not in excluded_tags and not (tag == "VBZ") and token.lower() not in stop_words:  # 'VBZ' es para el verbo en presente, 3ra persona singular
            abstract_terms.append(token.lower())
    
    # print("\nTérminos abstractos seleccionados:")
    # print(abstract_terms)

    return abstract_terms

def find_synonyms(word, abstract_dict):
    synonyms = []
    synsets = wordnet.synsets(word, lang='eng') # Create a list with words associated to the word
    for synset in synsets:
        for lemma in synset.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if word not in synonym and synonym not in abstract_dict:
                print(f"Possible synonym for {word}: {synonym}")
                synonyms.append(synonym)
    if not synonyms:
        return ["No suitable synonym found"]
    return synonyms

@app.get("/")
async def root_get():
    return "Hello world!"


@app.on_event("startup")
async def startup_event():
    global abstractWords, ZviAbstractWords, concreteWords, ZviConcreteWords

    # Cargar palabras abstractas
    listOfWords40000 = './xlsx/LIST WORDS FROM Concreteness ratings for 40 thousand generally known English word lemmas.xlsx'
    listOfWordsZvi = './xlsx/Abstract_Zvi_List.xlsx'
    abstractWords, concreteWords  = cargar_palabras_abstractas(listOfWords40000)
    ZviAbstractWords, ZviConcreteWords  = cargar_palabras_abstractas(listOfWordsZvi)
    abstractWords.update(ZviAbstractWords)
    concreteWords.update(ZviConcreteWords)


@app.post("/detect")
async def detect_abstract_words(item: Text):

    # Detectar palabras abstractas
    inputWords = set(detect_abstract_language_nltk(item.text))
    palabras_abstractas_encontradas = inputWords.intersection(abstractWords)

    # Agregar palabras abstractas compuestas presentes
    for word, (es_compuesta, _) in abstractWords.items():
        if (es_compuesta == 1) and (word in item.text) and (word not in palabras_abstractas_encontradas):
            palabras_abstractas_encontradas.add(word)
    
    # alternatives = {}
    # for word in palabras_abstractas_encontradas:
    #     synonym = find_synonyms(word, abstractWords)
    #     alternatives[word] = synonym

     
    # print("Alternatives found:", alternatives)

    return {"abstractWords": list(palabras_abstractas_encontradas)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
