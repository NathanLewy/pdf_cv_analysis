import os
import pdf2image
import pytesseract
import re

def extract_text_ocr(pdf_path):
    """
    Convertit un PDF en image et extrait le texte via OCR.
    """
    try:
        images = pdf2image.convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(img) for img in images])
        return text
    except Exception as e:
        print(f"Erreur OCR pour {pdf_path} : {e}")
        return ""

def clean_text(text):
    """
    Nettoie le texte extrait par OCR en supprimant les artefacts (nombres isolés, caractères indésirables).
    """
    text = text.strip()
    text = re.sub(r'[^A-Za-zÀ-ÖØ-öø-ÿ\s-]', '', text)  # Supprime les caractères non alphabétiques sauf espaces et tirets
    lines = text.split("\n")

    # Récupérer les premières lignes non vides
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line:
            return cleaned_line  # Retourne la première ligne utile

    return "Aucune ligne trouvée"

def extract_name_heuristic(text):
    """
    Extrait un nom basé sur une heuristique de détection.
    """
    words = text.split()
    if 2 <= len(words) <= 3:  # Un nom a généralement 2 ou 3 mots
        if all(word[0].isupper() for word in words):  # Vérifie les majuscules initiales
            return text
    return "Nom non trouvé"

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
        
        # Extraction via OCR
        extracted_text = extract_text_ocr(pdf_path)

        # Nettoyage du texte
        first_clean_line = clean_text(extracted_text)

        # Extraction du nom
        name = extract_name_heuristic(first_clean_line)

        print(f"📄 Fichier : {cv_file}")
        print(f"   📝 Première ligne nettoyée : {first_clean_line}")
        print(f"   🔍 Nom extrait : {name}\n")
