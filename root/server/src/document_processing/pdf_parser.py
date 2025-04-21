import pymupdf 
# pymupdf is faster than all other opensource data extraction packages and it supports pdf,docx,ppt
from pdf2image import convert_from_path
import os

class PdfProcessing:
    def __init__(self,file_path):
        try:
            with open(file_path, "rb") as file:
                self.name = file.name
                self.size = os.path.getsize(file_path)  
                self.doc = pymupdf.open(file)
                self.extracted_content = []
        except Exception as e:
            raise RuntimeError(f"PDF processing failed: {str(e)}")
        

    def process_pdf(self):
        for page_num, page in enumerate(self.doc):
             self.extracted_content.append({
                    "page_content": page.get_text(), 
                    "meta_data": {
                        "source": self.name + "__page_no_" + str(page_num)
                    }})
        return self.extracted_content     
            

    @staticmethod    
    def has_chart(page:pymupdf.Page)->bool:
       drawings = page.get_svg_image()
       if not drawings:
          return False
       return True
    @staticmethod
    def has_images(page:pymupdf.Page)->bool:
        images = page.get_images()
        if not images:
            return False
        return True
    @staticmethod
    def has_tables(page: pymupdf.Page)->bool:
        tables = page.find_tables().tables
        if not tables:
            return False
        return True
    
        
    






