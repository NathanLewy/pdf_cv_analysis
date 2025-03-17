import pdfplumber

def extract_pdf_text_with_pdfplumber(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            return text.replace("\n", " ")
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte : {e}")
        return ""

if __name__ == "__main__":
    pdf_file = "cvs/moi.pdf"
    extracted_text = extract_pdf_text_with_pdfplumber(pdf_file)
    print(extracted_text)
