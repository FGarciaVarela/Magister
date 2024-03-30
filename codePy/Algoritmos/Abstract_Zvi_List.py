import openpyxl

# Definir la lista de palabras
abstract_words = ["cognition", "cognitive", "motivation", "emotions", "emotional", "identity", "culture", "capabilities", "abilities", "skills", "assist", "intelligence", "goal", "aim", "support", "knowledge", "democracy", "personality", "availability", "available", "proud", "pride", "accountable", "think", "choice", "freedom", "collaborate", "collaboration", "fail", "successful", "owe", "curiosity", "creativity", "develop", "potential", "competence", "incompetence", "desire", "trust", "learning", "disability", "performance", "factors", "circumstances", "context", "meaning", "requirements", "assessment", "metacognition", "awareness", "pedagogy", "theoretical", "epistemology", "didactic", "moral", "efficacy", "multimodality", "communicative", "content", "competency", "capacity", "mindset", "wisdom", "experience", "understanding", "insight", "original", "ideas", "innovation", "empathy", "ethics", "resilience", "autonomy", "integrity", "comprehension", "authentic", "authenticity", "critical", "thinking", "efficiency", "brilliant", "attention", "concentration", "being", "present", "concentrate", "distraction", "stimulation", "interesting", "academic", "will", "soul", "helpless", "feeling", "problem", "challenge", "interest", "psychodidactic", "leader", "leadership", "excellence", "attention deficit disorder", "connect", "seriousness", "values", "success", "failure", "expectations", "empower", "faith", "believe", "belief", "ownership", "critical thinking", "imagination", "consciousness", "morality", "ethic", "ethical"]

# Crear un nuevo libro de trabajo de Excel
wb = openpyxl.Workbook()
ws = wb.active

# Agregar encabezados
ws.append(["Word", "Bigram", "Conc.M"])

# Iterar sobre la lista y agregar datos al archivo de Excel
for word in abstract_words:
    # Verificar si la palabra es compuesta
    tipo = 1 if ' ' in word else 0
    # Agregar fila al archivo de Excel
    ws.append([word, tipo, 1])

# Guardar el archivo de Excel
wb.save("Abstract_Zvi_List.xlsx")
