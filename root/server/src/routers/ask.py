from fastapi import APIRouter, Query, HTTPException
from collections import defaultdict
from pdf2image import convert_from_path
from ..config import constant
from ..services import qa_chain
from ..services import llm_calls
from ..prompts import ocr_prompt
from ..prompts import beautify_prompt

router = APIRouter()

def _parse_source_metadata(doc) -> tuple:
    """Extracts filename and page number from document metadata."""
    source = doc.metadata["source"]
    filename, page_info = source.split("__")
    page_num = page_info.split("-")[1]
    return filename, page_num

def _group_sources(docs) -> dict:
    """Groups documents by filename with associated page numbers."""
    grouped = defaultdict(set)
    for doc in docs:
        filename, page_num = _parse_source_metadata(doc)
        grouped[filename].add(page_num)
    return {k: sorted(v) for k, v in grouped.items()}

def _process_pdf_page(file_path: str, page_num: str):
    """Converts specific PDF page to OCR-processed text."""
    try:
        img = convert_from_path(
            file_path,
            first_page=int(page_num) + 1,
            last_page=int(page_num) + 1
        )
        prompt = ocr_prompt.prompt_ocr
        ocr_client = llm_calls.LlmCalls()
        print("it is working")
        return ocr_client.llm_ocr(img,prompt),
    except Exception as e:
        raise HTTPException(500, f"PDF processing failed: {str(e)}")



@router.post("/ask")
async def ask_question(question: str = Query(..., min_length=1)):
    """Handle document-based questions with citation support."""
    if not constant.global_state.vector_store:
        raise HTTPException(400, "No documents processed yet")

    # Retrieve relevant documents
    retriever = constant.global_state.vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)
    
    # # Process PDF pages with OCR
    # pdf_docs = [d for d in docs if any(ext in d.metadata['source'] for ext in [".pdf", ".docx", ".pptx"])]
    # grouped_files = _group_sources(pdf_docs)
    # for filename, pages in grouped_files.items():
    #     for page_num in pages:
    #         try:
    #             ocr_text = _process_pdf_page(filename, page_num)
    #             # Update document content with OCR text
    #             for doc in docs:
    #                 doc_filename, doc_page = _parse_source_metadata(doc)
    #                 if doc_filename == filename and doc_page == page_num:
    #                     doc.page_content = ocr_text
    #         except HTTPException:
    #             raise
    #         except Exception as e:
    #             raise HTTPException(500, f"Error processing {filename}: {str(e)}")

    # Generate answer
    sources = {f"{doc.metadata['source'][5:]}" for doc in docs}
    uniqe_sources :str= list(set(sources))
    source_str = "".join(uniqe_sources)
    chain = qa_chain.get_conversational_chain()
    response = chain.invoke({"input_documents": docs, "question": question})
    llm_client = llm_calls.LlmCalls()
    prompt = beautify_prompt.beautify_prompt(response["output_text"]+"sources are "+ source_str) 
    beutiful_response = llm_client.llm_response(prompt)
    print(beutiful_response)
    
    # Format sources

    
    return {
        "answer": beutiful_response 
    }
