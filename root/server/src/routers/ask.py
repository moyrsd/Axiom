from fastapi import APIRouter,Query, HTTPException
from ..config import constant
from ..services import qa_chain
router = APIRouter()

@router.post("/ask")
async def ask_question(question: str = Query(..., min_length=1)):
    """Handle questions via query parameter in POST"""
    if not constant.global_state.vector_store:
        raise HTTPException(400, "No documents processed yet")
    
    docs = constant.global_state.vector_store.similarity_search(question)
    chain = qa_chain.get_conversational_chain()
    response = chain({"input_documents": docs, "question": question})
    
    return {"answer": f"**Answer:**\n{response['output_text']}"}
