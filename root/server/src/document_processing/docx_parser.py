from docx import Document
from pdf2image import convert_from_path
import pytesseract


def process_docx(file_path: str) -> str:
    text = ""
    try:  # First try text extraction
        with open(file_path, "rb") as file:
            doc = Document(file)
            text += "\n".join([para.text for para in doc.paragraphs])
    except:  # Fallback to OCR
        images = convert_from_path(file_path)
        text += "".join([pytesseract.image_to_string(img) for img in images])
    return text