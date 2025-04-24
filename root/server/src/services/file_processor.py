import os
from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..services import vector_store
from ..config import constant
from ..document_processing import web_crawl
from docxtopdf import convert
from ..document_processing import (
    pdf_parser,
    image_parser,
    structured_data_parser,
    text_parser,
    ppt_parser
)

def process_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in [".pdf"]: 
        processor =pdf_parser.PdfProcessor(file_path)
        return processor.process_pdf()
    if ext in [".docx"]:
        output_file = file_path.replace(".docx", ".pdf")
        convert(file_path, output_file)
        processor =pdf_parser.PdfProcessor(output_file)
        return processor.process_pdf()
    if ext in [".pptx",".ppt"]:
        return ppt_parser.process_pptx(file_path)
    elif ext in (".xlsx", ".xls",".csv",".json"):
        return structured_data_parser.process_structured_data(file_path,ext)
    elif ext in (".png", ".jpg", ".jpeg"):
        return image_parser.process_image(file_path)
    elif ext == ".txt":
        return text_parser.process_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")    
    
def get_langchain_document(extracted_content):
    documents = [Document(
            page_content=item["page_content"],
            metadata=item["meta_data"]  
            ) for item in extracted_content]
    return documents


def get_docs_chunks(documents):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_documents(documents)


def process_files(temp_paths: List[str]):
    try:
        all_docs = []
        for path in temp_paths:
            all_docs.extend(process_file(path))
        # links = constant.global_state.links
        # all_docs.extend(web_crawl(links))
        lang_docs = get_langchain_document(all_docs)    
        chunked_docs = get_docs_chunks(lang_docs)
        vector_store.create_vector_store(chunked_docs)
        
    except Exception as e:
        print(f"Processing error: {str(e)}")





