from transformers import pipeline

# Initialize zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="roberta-large-mnli")

# Input sentences
sentences = [
    "We got a ton of earnings reports last week",
    "Life is full of learnings",
    "We had a terrific quarter, and our earnings per share were over 7 percent",
    "We strive to achieve results, and that is our goal, our motto",
    "i think the student has potential but the emotional and cognitive problems he has prevent him from developing his creativity.",
    "The cat is sitting on the windowsill, watching birds fly by.",
    "i want to develop a curriculum to strengthen the jewish identity of my students",
    "love is an art tha many intelligents can't achieve"
]


#etiquetas = ["concrete ideas", "subjective", "ambiguous words", "concrete words"]
etiquetas = ["concrete", "abstract", "ambiguous", "subjective", "not empirical", "not available to the senses"]
for sentence in sentences:
    # Perform zero-shot classification on the sentence with candidate labels
    #sentence = '"' + sentence + '"'
    classification = classifier(sentence, etiquetas)

    # Extract the labels and scores
    labels = classification["labels"]
    scores = classification["scores"]

    # Print the results
    print(f"Sentence: {sentence}")
    for label, score in zip(labels, scores):
        print(f"Detected {label} with {round(score * 100, 2)}% confidence")
    print()