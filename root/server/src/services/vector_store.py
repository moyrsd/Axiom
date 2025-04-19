from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from langchain_community.vectorstores import FAISS
from ..config import constant



def create_vector_store(text_chunks: List[str]):
    """Create and store FAISS vector store"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    if text_chunks:
        # Process in batches of 100
        batch_size = 100
        constant.global_state.vector_store = FAISS.from_texts(text_chunks[:batch_size], embedding=embeddings)
        
        for i in range(batch_size, len(text_chunks), batch_size):
            constant.global_state.vector_store.add_texts(text_chunks[i:i+batch_size])