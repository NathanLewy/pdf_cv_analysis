import os
import re
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
        return text.strip()  # Supprime les espaces vides en début/fin
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte ({pdf_path}): {e}")
        return ""

def extract_first_line(text):
    """
    Récupère la première ligne non vide du texte extrait.
    
    Args:
        text (str): Texte extrait du PDF.
    
    Returns:
        str: Première ligne non vide du texte.
    """
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            return line
    return "Aucune ligne trouvée"

def extract_name_heuristic(text):
    """
    Extrait le nom de la personne à partir du texte d'un CV en utilisant plusieurs heuristiques.
    
    Args:
        text (str): Texte extrait du CV.
        
    Returns:
        str: Nom extrait ou un message indiquant que le nom n'a pas été trouvé.
    """
    # Heuristique 1 : recherche des marqueurs "Prénom" et "Nom"
    first_name_pattern = re.compile(r"(?:Prénom|Prenom)\s*[:\-]\s*(?P<firstname>[A-ZÉÀÈÙ][a-zéàèùA-ZÉÀÈÙ]+)")
    last_name_pattern = re.compile(r"(?:Nom)\s*[:\-]\s*(?P<lastname>[A-ZÉÀÈÙ][a-zéàèùA-ZÉÀÈÙ]+(?:\s+[A-ZÉÀÈÙ][a-zéàèùA-ZÉÀÈÙ]+)?)")
    first_name_match = first_name_pattern.search(text)
    last_name_match = last_name_pattern.search(text)
    if first_name_match and last_name_match:
        full_name = f"{first_name_match.group('firstname')} {last_name_match.group('lastname')}".strip()
        return full_name

    # Heuristique 2 : recherche d'un pattern explicite "Nom:" ou "Name:" suivi d'un nom
    name_pattern = re.compile(r"(?:Nom|Name)\s*[:\-]\s*(?P<name>[A-ZÉÀÈÙ][a-zéàèùA-ZÉÀÈÙ\s'-]+)")
    match = name_pattern.search(text)
    if match:
        return match.group("name").strip()

    # Heuristique 3 : Analyse des premières lignes du document
    lines = text.splitlines()
    for line in lines[:10]:  # On analyse seulement les 10 premières lignes
        line = line.strip()
        if not line:
            continue
        words = line.split()
        if 2 <= len(words) <= 3:
            if all(word[0].isupper() for word in words):  # Vérifie les majuscules initiales
                return line
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
        extracted_text = extract_pdf_text(pdf_path)

        # Récupération de la première ligne du texte extrait
        first_line = extract_first_line(extracted_text)

        # Extraction du nom en utilisant l’heuristique
        name = extract_name_heuristic(extracted_text)

        print(f"📄 Fichier : {cv_file}")
        print(f"   🔍 Nom extrait : {name}\n")
