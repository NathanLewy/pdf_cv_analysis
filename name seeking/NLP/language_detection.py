import os
import spacy
from langdetect import detect
from pdfminer.high_level import extract_text

def extract_pdf_text(pdf_path):
    """
    Extrait le texte d'un fichier PDF en utilisant pdfminer.six.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte ({pdf_path}): {e}")
        return ""

def detect_language(text):
    """
    Détecte la langue du texte extrait.
    """
    try:
        lang = detect(text)
        return lang
    except Exception:
        return "unknown"

def extract_name_nlp(text, nlp):
    """
    Extrait le prénom et le nom de famille à partir du texte d'un CV en utilisant spaCy.
    
    Args:
        text (str): Texte extrait du CV.
        nlp (spacy.Language): Modèle NLP chargé.
    
    Returns:
        tuple: (prenom, nom) si détectés, ou ("Nom non trouvé", "Nom non trouvé")
    """
    doc = nlp(text)
    
    first_name = "Nom non trouvé"
    last_name = "Nom non trouvé"
    
    for ent in doc.ents:
        if ent.label_ == "PER":  # "PER" = Personne
            parts = ent.text.split()
            if len(parts) >= 2:
                first_name = parts[0]
                last_name = " ".join(parts[1:])
                break  # Prend le premier nom valide détecté
    
    return first_name, last_name

if __name__ == "__main__":
    cv_folder = "cvs"  # Dossier contenant les CVs

    # Vérifier si le dossier existe
    if not os.path.exists(cv_folder):
        print(f"Erreur : Le dossier {cv_folder} n'existe pas.")
        exit()

    # Liste des fichiers PDF dans le dossier
    cv_files = [f for f in os.listdir(cv_folder) if f.endswith(".pdf")]

    if not cv_files:
        print("Aucun fichier PDF trouvé dans le dossier cvs.")
        exit()

    print("\n📌 Résultats de l'extraction des noms :\n")

    for cv_file in cv_files:
        pdf_path = os.path.join(cv_folder, cv_file)

        # Extraction du texte depuis le PDF
        extracted_text = extract_pdf_text(pdf_path)

        # Détection de la langue du texte
        detected_lang = detect_language(extracted_text)

        # Charger le bon modèle NLP selon la langue détectée
        if detected_lang == "fr":
            nlp = spacy.load("fr_core_news_md")
            lang_label = "🇫🇷 Français"
        elif detected_lang == "en":
            nlp = spacy.load("en_core_web_md")
            lang_label = "🇬🇧 Anglais"
        else:
            print(f"📄 Fichier : {cv_file} - 🌍 Langue inconnue, impossible d'analyser.")
            continue

        # Extraction du prénom et du nom via NLP
        first_name, last_name = extract_name_nlp(extracted_text, nlp)

        print(f"📄 Fichier : {cv_file} ({lang_label})")
        print(f"   🔍 Prénom : {first_name}")
        print(f"   🔍 Nom : {last_name}\n")
