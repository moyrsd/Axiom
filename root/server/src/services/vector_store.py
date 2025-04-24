from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
from ..config import constant

def create_vector_store(documents: List[Document]):  # Accept Documents instead of raw text
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    if hasattr(constant.global_state, 'vector_store') and constant.global_state.vector_store:
        constant.global_state.vector_store.add_documents(documents)
    else :
        if documents:
            vector_store = Chroma.from_documents(
                documents=documents,  # Directly use Documents
                embedding=embeddings,
                persist_directory="./chroma_db",
                collection_name="document_embeddings"
            )
            # print(vector_store)
            constant.global_state.vector_store = vector_store
    constant.global_state.vector_store.persist()        


# https://python.langchain.com/docs/integrations/vectorstores/chroma/
