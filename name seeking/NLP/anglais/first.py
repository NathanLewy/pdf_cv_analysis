import re
import spacy
from pdfminer.high_level import extract_text

def extract_pdf_text(pdf_path):
    """
    Extrait le texte d'un PDF en utilisant pdfminer.six.
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF.
        
    Returns:
        str: Texte extrait.
    """
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte: {e}")
        return ""

def clean_text(text):
    """
    Uniformise le texte en remplaçant les espaces multiples et retire les caractères parasites en début de texte.
    """
    text = re.sub(r'\s+', ' ', text)                     # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'^[^A-Za-zÀ-ÖØ-öø-ÿ]+', '', text)     # Retirer les caractères non alphabétiques au début
    return text.strip()

def extract_name(header_text, nlp):
    """
    Extrait le prénom et le nom de famille à partir du header du CV.
    
    La méthode consiste à :
      1. Séparer le header en tokens.
      2. Ignorer les tokens de moins de 2 caractères (pour éviter des artefacts comme "é").
      3. Prendre le premier token valide comme prénom et le second comme nom de famille.
      4. Si cette heuristique échoue, utiliser spaCy pour tenter de détecter une entité PERSON dans le header.
    
    Args:
        header_text (str): Texte du header extrait du CV.
        nlp (spacy.Language): Modèle NLP chargé.
    
    Returns:
        tuple: (prénom, nom de famille) ou (None, None) si non détecté.
    """
    tokens = header_text.split()
    # Filtrer les tokens trop courts (par exemple, de longueur < 2)
    name_tokens = [token for token in tokens if len(token) >= 2 and re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+$', token)]
    
    if len(name_tokens) >= 2:
        # On prend le premier token comme prénom, et le deuxième comme nom de famille.
        return name_tokens[0], name_tokens[1]
    
    # Fallback : utiliser spaCy sur le header pour détecter une entité PERSON
    doc = nlp(header_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            parts = ent.text.split()
            # Vérifier que le premier token est suffisamment long
            if parts and len(parts[0]) >= 2:
                return parts[0], " ".join(parts[1:]) if len(parts) >= 2 else None
    return None, None

def get_name_from_text(text, nlp):
    """
    Isole le header du CV et en extrait le prénom et le nom de famille.
    
    On considère que le header correspond à la partie du texte avant le mot-clé " E X P E R I E N C E".
    
    Args:
        text (str): Texte nettoyé extrait du CV.
        nlp (spacy.Language): Modèle NLP chargé.
    
    Returns:
        tuple: (prénom, nom de famille) ou (None, None) si non détecté.
    """
    if " E X P E R I E N C E" in text:
        header = text.split(" E X P E R I E N C E")[0]
    else:
        header = text
    return extract_name(header, nlp)

if __name__ == "__main__":
    pdf_file = "cvs/ethan.pdf"  # Remplace par le chemin vers ton CV
    raw_text = extract_pdf_text(pdf_file)
    cleaned_text = clean_text(raw_text)
    
    # Affichage pour vérification
    print("Texte nettoyé :", cleaned_text)
    
    # Charger le modèle spaCy anglais (si le CV est en anglais)
    nlp = spacy.load("en_core_web_trf")
    
    first_name, last_name = get_name_from_text(cleaned_text, nlp)
    print(f"Fichier : {pdf_file}")
    print(f"Prénom détecté : {first_name}")
    print(f"Nom de famille détecté : {last_name}")
