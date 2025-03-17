import openai

# Remplace la clé par la tienne
openai.api_key = "sk-aPH7DC0mCzcKUZMMjTGG97xnEdj4MEYfLjBjY5RnFtT3BlbkFJOHbGOqLbFtlkN4gd0L2c012yGCupXyG51z8nK8UdMA"

try:
    # Utiliser la nouvelle interface (nouvelle structure de requête)
    response = openai.completions.create(
        model="gpt-3.5-turbo",
        prompt="Hello, world!",
        max_tokens=5
    )
    print("Réponse obtenue :", response['choices'][0]['text'])
except Exception as e:
    print(f"Erreur inconnue : {e}")
