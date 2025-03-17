from pdfminer.high_level import extract_text

def extract_pdf_text(pdf_path):
    """
    Extrait le texte d'un fichier PDF en utilisant pdfminer.six.
    Le texte extrait tente de conserver la mise en page originale.

    Args:
        pdf_path (str): Chemin vers le fichier PDF.

    Returns:
        str: Texte extrait du PDF.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte : {e}")
        return ""

if __name__ == "__main__":
    pdf_file = "cvs/nathan.pdf" 
    extracted_text = extract_pdf_text(pdf_file)
    print(extracted_text)

