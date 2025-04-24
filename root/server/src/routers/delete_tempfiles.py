from fastapi import HTTPException, APIRouter
from pathlib import Path
import shutil
import os
router = APIRouter()
from ..config import constant

# During startup delete the last session files as we are not storing for every user
@router.post("/removetempfiles")
async def cleanup_system():
    """Clean both temp files and ChromaDB directory"""
    print()
    try:
        # 1. Clean upload temp files
        temp_files = [f for f in os.listdir() if f.startswith("temp_")]
        for temp_file in temp_files:
            os.remove(temp_file)
            print(f"Deleted temp file: {temp_file}")

        # 2. Clean ChromaDB directory
        constant.global_state.vector_store = None  ## Deleting vector store from memory
        chroma_path = Path("./chroma_db")
        if chroma_path.exists():
            shutil.rmtree(chroma_path)
            print(f"Deleted ChromaDB directory: {chroma_path}")
        else :
            print("ChromaDB does not exist")    

        return {"status": "Cleanup successful"}
        
    except Exception as e:
        raise HTTPException(500, f"Cleanup failed: {str(e)}")
