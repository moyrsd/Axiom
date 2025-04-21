import pymupdf
from pdf2image import convert_from_path
import os
from pathlib import Path
import logging
from typing import List, Dict
from ..services import llm_calls
from ..prompts import ocr_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PdfProcessor:
    """High-performance PDF processor with fallback to OCR for text extraction."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate_file()
        self.doc: pymupdf.Document = None
        self._open_pdf()

    def _validate_file(self) -> None:
        """Ensure valid PDF file exists."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() != ".pdf":
            raise ValueError("Invalid file format. Only PDFs are supported.")

    def _open_pdf(self) -> None:
        """Safely open PDF file using context manager."""
        try:
            self.doc = pymupdf.open(self.file_path)
        except Exception as e:
            logger.error(f"Failed to open PDF: {self.file_path}")
            raise RuntimeError(f"PDF open failed: {str(e)}") from e

    def process_pdf(self) -> List[Dict]:
        """Process all pages with text extraction and OCR fallback."""
        extracted_content = []
        
        for page_num in range(len(self.doc)):
            try:
                page = self.doc.load_page(page_num)
                content = self._process_page(page, page_num)
                extracted_content.append(content)
            except Exception as e:
                logger.warning(f"Error processing page {page_num}: {str(e)}")
                continue
        
        return extracted_content

    def _process_page(self, page: pymupdf.Page, page_num: int) -> Dict:
        """Process individual page with multiple extraction strategies."""
        # if self._needs_ocr(text):
        #     logger.info(f"Using OCR for page {page_num}")
        #     text = self._extract_text_via_ocr(page_num)
        # else:
        text = self._extract_text(page)    
        # print(text)
        return {
            "page_content": text,
            "meta_data": self._build_metadata(page_num)
        }

    def _extract_text(self, page: pymupdf.Page) -> str:
        """Extract text using PyMuPDF with layout preservation."""
        return page.get_text("text", sort=True)

    def _needs_ocr(self, text: str) -> bool:
        """Determine if OCR is needed based on extracted text quality."""
        return len(text.strip().split()) <= 10

    def _extract_text_via_ocr(self, page_num: int) -> str:
        """Perform OCR on page image using LLM."""
        try:
            image = self._convert_page_to_image(page_num)
            return llm_calls.LlmCalls().llm_ocr(image, ocr_prompt.prompt_ocr)
        except Exception as e:
            logger.error(f"OCR failed for page {page_num}: {str(e)}")
            return "OCR text extraction failed"

    def _convert_page_to_image(self, page_num: int):
        """Convert PDF page to high-quality image."""
        return convert_from_path(
            self.file_path,
            first_page=page_num + 1,
            last_page=page_num + 1,
        )[0]

    def _build_metadata(self, page_num: int) -> Dict:
        """Generate standardized metadata for each page."""
        return {
            "source": f"{self.file_path.name}__pageno-{page_num+1}",
            "file_size": os.path.getsize(self.file_path),
            "file_path": str(self.file_path.resolve())
        }

