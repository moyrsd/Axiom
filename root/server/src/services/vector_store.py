from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
from ..config import constant
import os
import uuid
import datetime

def create_vector_store(documents: List[Document]):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        
        # Create a unique directory name using timestamp and UUID
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]  # Take first 8 chars of UUID for brevity
        unique_dir = f"chroma_db_{timestamp}_{unique_id}"
        
        # Use absolute path for better consistency
        persist_directory = os.path.abspath(f"./{unique_dir}")
        print(f"Creating new ChromaDB at: {persist_directory}")
        
        # Create directory with explicit permissions
        os.makedirs(persist_directory, exist_ok=True, mode=0o755)
        
        # Create vector store with the documents
        if documents:
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=persist_directory,
                collection_name="document_embeddings"
            )
            print(f"Created new ChromaDB directory at {persist_directory}")
        else:
            vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings,
                collection_name="document_embeddings"
            )
            print(f"Initialized empty ChromaDB at {persist_directory}")
        
        # Save to global state
        constant.global_state.vector_store = vector_store
        
        # Optionally save the path for later reference
        constant.global_state.vector_store_path = persist_directory
        
        
        print(f"Vector store initialized: {constant.global_state.vector_store}")
        return vector_store
        
    except Exception as e:
        print(f"Vector store error: {str(e)}")
        raise e