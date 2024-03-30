import pandas as pd
import spacy

# Función para cargar palabras abstractas desde un archivo XLSX
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


# Cargamos SpaCy el cual es para tokenizar (separar) y procesar lenguaje natural.
# Versión trf más pesada pero más eficaz que "en_core_web_sm"
nlp = spacy.load("en_core_web_trf")

def detect_abstract_language_spacy(text):
    abstract_terms = []
    doc = nlp(text)
    lista =[]
    for token in doc:
        lista.append((token, token.pos_))
        # Excluir de la frase preposiciones, pronombres posesivos, pronombres personales, determinantes, conjunciones coordinantes,verbos particulares, subordinating conjunction, y verbos en presente 3ra persona singular
        if token.pos_ not in ["PRON", "DET", "CCONJ", "ADP", "PART", "SCONJ"] and not (token.pos_ == "VERB" and token.tag_ == "VBZ"):
            abstract_terms.append(token.text.lower())
    print(lista)
    print("\n")
    return abstract_terms


if __name__ == "__main__":

    listOfWords40000 = './csv/LIST WORDS FROM Concreteness ratings for 40 thousand generally known English word lemmas.xlsx'
    abstractWords = cargar_palabras_abstractas(listOfWords40000)

    listOfWordsZvi = './csv/Abstract_Zvi_List.xlsx'
    ZviAbstractWords = cargar_palabras_abstractas(listOfWordsZvi)

    print("Primeras 3 entradas del diccionario:")
    count = 0
    for palabra in abstractWords.items():
        print("Palabra:", palabra[0])
        print("Compuesta?:", palabra[1][0])
        print("Concreteness:", palabra[1][1])
        print()
        count += 1
        if count == 3:
            break

    inputText = input("Ingrese una frase de texto: ")

    abstractWords.update(ZviAbstractWords)

    Inputwords = set(detect_abstract_language_spacy(inputText))

    #Intesección palabras spacy y diccionario abstracto. Agrega palabras simples (no compuestas)
    palabras_abstractas_encontradas = Inputwords.intersection(abstractWords)


    # Agregar palabras abstractas compuestas presentes
    for word, (es_compuesta, _) in abstractWords.items():
        if (es_compuesta == 1) and (word in inputText) and (word not in palabras_abstractas_encontradas):
            palabras_abstractas_encontradas.add(word)


    # Imprimir palabras abstractas encontradas
    if palabras_abstractas_encontradas:
        print(f"Palabras abstractas encontradas:{palabras_abstractas_encontradas}")
    else:
        print("No se encontraron palabras abstractas en la frase.")
