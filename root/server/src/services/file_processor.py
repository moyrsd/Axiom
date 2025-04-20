import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..services import vector_store
from ..document_processing import (
    pdf_parser,
    docx_parser,
    pptx_parser,
    excel_parser,
    csv_parser,
    json_parser,
    image_parser,
    text_parser,
)

def process_file(file_path: str) -> str:
    text = ""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        processor = pdf_parser.PdfProcessing(file_path) 
        extracted_content = processor.process_pdf() 
        for content in extracted_content:
            text += content["page_content"] + "\n" 
    elif ext == ".docx":
        text += docx_parser.process_docx(file_path)
    elif ext == ".pptx":
        text += pptx_parser.process_pptx(file_path)
    elif ext in (".xlsx", ".xls"):
        text += excel_parser.process_excel(file_path)
    elif ext == ".csv":
        text += csv_parser.process_csv(file_path)
    elif ext == ".json":
        text += json_parser.process_json(file_path)
    elif ext in (".png", ".jpg", ".jpeg"):
        text += image_parser.process_image(file_path)
    elif ext == ".txt":
        text += text_parser.process_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")    
    
    return text



def get_text_chunks(text: str) -> List[str]:
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_text(text)


def process_files(temp_paths: List[str]):
    try:
        raw_text = ""
        for path in temp_paths:
            raw_text += process_file(path) + "\n\n"
        
        text_chunks = get_text_chunks(raw_text)
        vector_store.create_vector_store(text_chunks)
        
        # Cleanup
        for path in temp_paths:
            os.remove(path)
            
    except Exception as e:
        print(f"Processing error: {str(e)}")




