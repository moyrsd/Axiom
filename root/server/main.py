from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store (for development only)
vector_store = None

def get_pdf_text(file_paths: List[str]) -> str:
    """Extract text from PDF files"""
    text = ""
    for path in file_paths:
        with open(path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    return text

def get_text_chunks(text: str) -> List[str]:
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_text(text)

def create_vector_store(text_chunks: List[str]):
    """Create and store FAISS vector store"""
    global vector_store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    if text_chunks:
        # Process in batches of 100
        batch_size = 100
        vector_store = FAISS.from_texts(text_chunks[:batch_size], embedding=embeddings)
        
        for i in range(batch_size, len(text_chunks), batch_size):
            vector_store.add_texts(text_chunks[i:i+batch_size])

def get_conversational_chain():
    """Create QA chain with prompt template"""
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    Context: {context}
    Question: {question}
    
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

@app.post("/upload")
async def upload_pdf(
    files: List[UploadFile] = File(...), 
    background_tasks: BackgroundTasks = None
):
    """Handle PDF upload and processing"""
    try:
        # Save uploaded files temporarily
        temp_paths = []
        for file in files:
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            temp_paths.append(temp_path)
        
        # Add background processing task
        if background_tasks:
            background_tasks.add_task(process_files, temp_paths)
            return {"status": "Processing started"}
        
        raise HTTPException(500, "Background tasks not available")
    
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")

def process_files(temp_paths: List[str]):
    """Process files in background"""
    try:
        # Extract and process text
        raw_text = get_pdf_text(temp_paths)
        text_chunks = get_text_chunks(raw_text)
        create_vector_store(text_chunks)
        
        # Cleanup temporary files
        for path in temp_paths:
            if os.path.exists(path):
                os.remove(path)
                
    except Exception as e:
        print(f"Processing error: {str(e)}")



@app.post("/ask")
async def ask_question(question: str = Query(..., min_length=1)):
    """Handle questions via query parameter in POST"""
    if not vector_store:
        raise HTTPException(400, "No documents processed yet")
    
    docs = vector_store.similarity_search(question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": question})
    
    return {"answer": f"**Answer:**\n{response['output_text']}"}

