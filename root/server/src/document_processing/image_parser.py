import pytesseract
from PIL import Image

def process_image(file_path: str) -> str:
    text = ""
    text+= pytesseract.image_to_string(Image.open(file_path))
    return text