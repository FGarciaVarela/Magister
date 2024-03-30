import spacy
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="roberta-large-mnli")

# Download NLTK resources if not already downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

# Cargamos SpaCy el cual es para tokenizar (separar) y procesar lenguaje natural.
# Versión trf más pesada pero más eficaz que "en_core_web_sm"
nlp = spacy.load("en_core_web_trf")


def detect_abstract_language_spacy(text):
    abstract_terms = []
    tokenText = nlp(text)
    for token in tokenText:
        # tomar solo adjetivos, verbos, etc
        if token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB', 'ADV'] and not token.is_stop:
            # ver si atributos, objetos de preposición, complemento del predicado, etc tienen dependendcia
            # sintáctica mediante el etiquetado del token, y ver así si se relaciona con palabras cercanas /contexto cercano
            if token.dep_ not in ["attr", "dobj", "pobj", "nsubj", "ccomp", "xcomp"]:
                abstract_terms.append(token.text)
    print("Abstract terms detected by SpaCy:", abstract_terms)
    return abstract_terms

#################################################################################################################################################


def detect_abstract_language_nltk(text):
    abstract_terms = []

    # Function to check if a word is abstract
    def is_abstract(word):
        # Obtener los synsets para la palabra
        synsets = wordnet.synsets(word)

        # Clasificaciones POS relevantes
        # 'n' para noun, 's' para adjective, 'r' para adverb, 'v' para verb
        relevant_pos = ['n', 's', 'r', 'v']

        # Check if any synset has an abstract definition with relevant POS or hypernyms
        for synset in synsets:
            # Verificar si la parte del discurso es relevante
            if synset.pos() in relevant_pos:
                return True
            # Verificar si hay hypernyms
            for hypernym in synset.hypernyms():
                if hypernym:
                    return True
        return False

    # Function to identify abstract terms in text
    def find_abstract_terms(text):
        abstract_terms = []

        # Tokenizar texto
        words = word_tokenize(text)

        # Get English stopwords
        stop_words = set(stopwords.words('english'))

        # hacer el tagg de la tokenización
        tagged_words = pos_tag(words)

        # Iterate through each tagged word
        for word, tag in tagged_words:
            # Check if the word is not a stopword, not a pronoun, and not punctuation
            if word.lower() not in stop_words and tag in ['NN', 'NNS', 'JJ', 'RB', 'VB', 'VBN', 'VBG']:
                # Check if the word is abstract
                if is_abstract(word):
                    abstract_terms.append(word)
        return abstract_terms
    abstract_terms = find_abstract_terms(text)
    print("Abstract terms detected by NLTK:", abstract_terms)
    return abstract_terms

##############################################################################################################################################


def zero_shot(text):
    classification = classifier(text, ["concrete ideas", "subjective", "ambiguous words", "concrete words"])
    abstract_scores = [classification["scores"][i] for i, label in enumerate(classification["labels"]) if label in ["subjective", "ambiguous words"]]
    concrete_scores = [classification["scores"][i] for i, label in enumerate(classification["labels"]) if label in ["concrete ideas", "concrete words"]]
    
    if sum(abstract_scores) > 0.3:
        return True, round(sum(abstract_scores) * 100, 2)
    else:
        return False, round(sum(concrete_scores) * 100, 2)

##############################################################################################################################################


def suggest_concretization(abstract_terms, text):
    def answerText():
        print("In the following text prompt, these words/ideas were found as abstract:", abstract_terms)
        print("Is each word concrete, based on evidence rigorous as in empirical research in the hard sciences?")
        print(text)
    choice = input("Choose an option: \n1. Show results only\n2. Show results with suggestions to improve abstraction\nEnter your choice (1 or 2): ")

    if choice == '1':
        answerText()
    elif choice == '2':
        print("Help me changing the abstract ideas for more concrete ones, eviting abstract terms")
        answerText()
        
    else:
        print("Invalid choice. Showing results only.")
        answerText()


    # Aquí se agregará ChatGpt para hacer las sugerencias de cada término


def main():
    text = input("Enter your text: ")
    quotedText = '"' + text + '"'
    print(quotedText)
    zeroBolean, percentege = zero_shot(quotedText)
    if zeroBolean:
        print(f"It was detected {percentege}% of abstraction")
        abstract_terms_spacy = set(detect_abstract_language_spacy(quotedText))
        abstract_terms_roberta = set(detect_abstract_language_nltk(quotedText))

        abstract_terms_final = abstract_terms_spacy.intersection(
            abstract_terms_roberta)

        if abstract_terms_final:
            suggest_concretization(abstract_terms_final, text)
        else:
            print("No abstract terms detected in the text.")

    else:
        print(f"Good! It was detected {percentege}% as concrete")


if __name__ == "__main__":
    main()
