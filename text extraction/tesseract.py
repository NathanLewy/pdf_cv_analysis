import pdf2image
import pytesseract

def extract_text_ocr(pdf_path):
    try:
        images = pdf2image.convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(img) for img in images])
        return text
    except Exception as e:
        print(f"Erreur OCR : {e}")
        return ""

if __name__ == "__main__":
    pdf_file = "cvs/pierre.pdf"
    extracted_text = extract_text_ocr(pdf_file)
    print(extracted_text)
