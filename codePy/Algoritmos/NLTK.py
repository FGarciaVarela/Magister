import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download NLTK resources if not already downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

# Function to check if a word is abstract


def is_abstract(word):
    # Obtener los synsets para la palabra
    synsets = wordnet.synsets(word)

    # Clasificaciones POS relevantes
    # 'n' para noun, 's' para adjective, 'r' para adverb, 'v' para verb
    relevant_pos = ['n', 's', 'r', 'v']

    for synset in synsets:
        # Verificar si la parte del discurso es relevante y si es un hyperterm (palabra que está dentro/relacionada con otra, ej: perro se relaciona con golden, pastor aleman, etc)
        if synset.pos() in relevant_pos and synset.hypernyms():
            return True
    return False


# Function to identify abstract terms in text
def find_abstract_terms(text):
    abstract_terms = []

    # Tokenize the text into words
    words = word_tokenize(text)

    # Get English stopwords
    stop_words = set(stopwords.words('english'))

    # Perform part-of-speech tagging
    tagged_words = pos_tag(words)

    print(tagged_words)

    # Iterate through each tagged word
    for word, tag in tagged_words:
        # Check if the word is not a stopword, not a pronoun, and not punctuation
        if word.lower() not in stop_words and tag in ['NN', 'NNS', 'JJ', 'RB', 'VB', 'VBN', 'VBG']:
            # Check if the word is abstract
            if is_abstract(word):
                abstract_terms.append(word)

    return abstract_terms


# Example text
text = "i think the student has potential but the emotional and cognitive problems he has prevent him from developing his creativity."

# Find abstract terms in the text
abstract_terms = find_abstract_terms(text)

# Print the abstract terms found
print("Abstract terms found:", abstract_terms)
