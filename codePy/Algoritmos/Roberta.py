import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, AdamW
from torch.utils.data import DataLoader, TensorDataset

# Load pre-trained RoBERTa tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=2)

# Define a list of abstract words
abstract_words = ["cognition", "cognitive", "motivation", "emotions", "emotional", "identity", "culture", "capabilities", "abilities", "skills", "assist", "intelligence", "goal", "aim", "support", "knowledge", "democracy", "personality", "availability", "available", "proud", "pride", "accountable", "think", "choice", "freedom", "collaborate", "collaboration", "fail", "successful", "owe", "curiosity", "creativity", "develop", "potential", "competence", "incompetence", "desire", "trust", "learning", "disability", "performance", "factors", "circumstances", "context", "meaning", "requirements", "assessment", "metacognition", "awareness", "pedagogy", "theoretical", "epistemology", "didactic", "moral", "efficacy", "multimodality", "communicative", "content", "competency",
                  "capacity", "mindset", "wisdom", "experience", "understanding", "insight", "original", "ideas", "innovation", "empathy", "ethics", "resilience", "autonomy", "integrity", "comprehension", "authentic", "authenticity", "critical", "thinking", "efficiency", "brilliant", "attention", "concentration", "being", "present", "concentrate", "distraction", "stimulation", "interesting", "academic", "will", "soul", "helpless", "feeling", "problem", "challenge", "interest", "psychodidactic", "leader", "leadership", "excellence", "attention deficit disorder", "connect", "seriousness", "values", "success", "failure", "expectations", "empower", "faith", "believe", "belief", "ownership", "critical thinking", "imagination", "consciousness", "morality", "ethic", "ethical"]

concrete_examples = ["We got a ton of earnings reports last week",
"We strive to achieve results, and that is our goal, our motto",
"The cat is sitting on the windowsill, watching birds fly by."]
abstract_examples = ["Life is full of learnings",
"We had a terrific quarter, and our earnings per share were over 7 percent",
"i think the student has potential but the emotional and cognitive problems he has prevent him from developing his creativity.",
"i want to develop a curriculum to strengthen the jewish identity of my students",
"love is an art tha many intelligents can't achieve"]

# Function to ask user for confirmation and save the result
def save_result(result):

    while True:
        save = input(
            "Do you want to save this result as concrete (c), abstract (a), or skip (s)? ")
        if save.lower() == 'c':
            with open('concrete_examples.csv', 'a') as f:
                f.write(result + '\n')
            print("Result saved as concrete.")
            break
        elif save.lower() == 'a':
            with open('abstract_examples.csv', 'a') as f:
                f.write(result + '\n')
            print("Result saved as abstract.")
            break
        elif save.lower() == 's':
            print("Skipping this result.")
            break
        else:
            print(
                "Invalid input. Please enter 'c' for concrete, 'a' for abstract, or 's' to skip.")

# Function to tokenize
def classify_text(input_text):
    # Tokenize and encode input text
    input_ids = tokenizer.encode(
        input_text, add_special_tokens=True, truncation=True, max_length=128, return_tensors='pt')
    # Predict the label for the input text
    outputs = model(input_ids)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_label = torch.argmax(probabilities, dim=1).item()

    return predicted_label

# Function to fine-tune the model

def fine_tune_model(train_dataset):
    # Define DataLoader for training set
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

    # Define optimizer and loss function
    optimizer = AdamW(model.parameters(), lr=5e-5)

    # Fine-tune RoBERTa model
    num_epochs = 3
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        for input_ids, attention_mask, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(
                input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()
            optimizer.step()
        avg_train_loss = total_loss / len(train_loader)
        print(
            f'Epoch {epoch+1}/{num_epochs}, Avg Train Loss: {avg_train_loss:.4f}')


# Load pre-trained RoBERTa tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained(
    'roberta-base', num_labels=2)

# Function to convert examples to numerical representations and create dataset
def prepare_dataset(abstract_examples, concrete_examples):
    # Convert abstract examples to numerical representations
    abstract_inputs = tokenizer(abstract_examples, padding=True, truncation=True, return_tensors="pt")
    abstract_labels = torch.tensor([0] * len(abstract_examples))  # Label 0 for abstract

    # Convert concrete examples to numerical representations
    concrete_inputs = tokenizer(concrete_examples, padding=True, truncation=True, return_tensors="pt")
    concrete_labels = torch.tensor([1] * len(concrete_examples))  # Label 1 for concrete

    # Combine abstract and concrete examples into a single dataset
    all_input_ids = torch.cat((abstract_inputs['input_ids'], concrete_inputs['input_ids']), dim=0)
    all_attention_masks = torch.cat((abstract_inputs['attention_mask'], concrete_inputs['attention_mask']), dim=0)
    all_labels = torch.cat((abstract_labels, concrete_labels), dim=0)

    # Create TensorDataset
    train_dataset = TensorDataset(all_input_ids, all_attention_masks, all_labels)

    return train_dataset

print("Program terminated.")


if __name__ == "__main__":
    