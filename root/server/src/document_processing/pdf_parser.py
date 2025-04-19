from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract


def process_pdf(file_path: str) -> str:
    text = ""
    try:  # First try text extraction
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            text += "".join([page.extract_text() or "" for page in pdf_reader.pages])
    except:  # Fallback to OCR
        images = convert_from_path(file_path)
        text += "".join([pytesseract.image_to_string(img) for img in images])
    return text