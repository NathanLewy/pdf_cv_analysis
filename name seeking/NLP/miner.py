import os
import spacy
from pdfminer.high_level import extract_text

def extract_pdf_text(pdf_path):
    """
    Extrait le texte d'un fichier PDF en utilisant pdfminer.six.
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF.
    
    Returns:
        str: Texte extrait du PDF.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte ({pdf_path}): {e}")
        return ""

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
    
    # Parcours des entités détectées par spaCy
    for ent in doc.ents:
        if ent.label_ == "PER":  # "PER" = entité de type personne
            parts = ent.text.split()
            if len(parts) >= 2:
                first_name = parts[0]
                last_name = " ".join(parts[1:])
                break  # On prend le premier nom valide détecté
    
    return first_name, last_name

if __name__ == "__main__":
    cv_folder = "cvs"  # Dossier contenant les CVs

    # Charger le modèle NLP pour éviter de le recharger à chaque fichier
    nlp = spacy.load("fr_core_news_md")

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

        # Extraction du prénom et du nom via NLP
        first_name, last_name = extract_name_nlp(extracted_text, nlp)

        print(f"📄 Fichier : {cv_file}")
        print(f"   🔍 Prénom : {first_name}")
        print(f"   🔍 Nom : {last_name}\n")
