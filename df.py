from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Spécifier explicitement que l'on utilise SentencePiece
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner", force_download=True)
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Exemple de texte
text = "Nathan Lewy a étudié à l'Université de Lorraine."

# Extraction des noms
entities = nlp(text)
names = [entity['word'] for entity in entities if entity['entity_group'] == "PER"]

print(f"Noms et prénoms trouvés : {' '.join(names)}")
