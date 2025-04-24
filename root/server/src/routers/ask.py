from fastapi import APIRouter, Query, HTTPException
from ..config import constant
from ..services import qa_chain
from ..services import llm_calls
from ..prompts import beautify_prompt,dataprocessing_prompt
from ..document_processing import structured_data_parser
from ..services import convert_to_json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from ..config import constant
import os

router = APIRouter()

@router.post("/ask")
async def ask_question(question: str = Query(..., min_length=1)):
    
    if not constant.global_state.vector_store:
        raise HTTPException(400, "No documents processed yet")
    
    response, source_str = rag_response(question)
    print(response)
    # print(response)
    need =_needs_data_processing(response,question,constant.global_state.temp_paths)
    print(need)
    if (need["data_processing_needed"]=="yes"):
        response= structured_data_parser.process_structured_data(need["filename"],str(need["ext"]),action="data_processing",question=question)
        source_str = str(need["filename"][5:]) 
    return {
        "answer": beutify(response,source_str,question)
    }



def rag_response(question):
    try:
        # Check if vector store exists in memory
        if not constant.global_state.vector_store:
            # Try to load from disk if it exists
            embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
            if os.path.exists("./chroma_db"):
                constant.global_state.vector_store = Chroma(
                    persist_directory="./chroma_db",
                    embedding_function=embeddings,
                    collection_name="document_embeddings"
                )
            else:
                raise HTTPException(400, "No documents processed yet")
        
        retriever = constant.global_state.vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(question)
        sources = {f"{doc.metadata['source'][5:]}" for doc in docs}
        unique_sources = list(set(sources))
        source_str = "".join(unique_sources)
        chain = qa_chain.get_conversational_chain()
        response = chain.invoke({"input_documents": docs, "question": question})
        response_text = response["output_text"]
        return response_text, source_str  # Return a proper tuple
    except Exception as e:
        print(f"Error in rag_response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

def beutify(response,source_str,question):
    llm_client = llm_calls.LlmCalls()
    prompt = beautify_prompt.beautify_prompt(response+"sources are "+ source_str,question)
    print(prompt) 
    return llm_client.llm_response(prompt)


def _needs_data_processing(previous_answer: str, question: str, file_names=None):
    llm_client = llm_calls.LlmCalls()
    prompt = dataprocessing_prompt.data_processing_prompt(previous_answer,question,file_names)
    data_processing = llm_client.llm_response(prompt)
    data_processing_json = convert_to_json.convert(data_processing)
    return data_processing_json

    







# https://python.langchain.com/docs/tutorials/chatbot/
# https://python.langchain.com/docs/tutorials/agents/



