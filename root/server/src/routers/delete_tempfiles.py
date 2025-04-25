from fastapi import HTTPException, APIRouter
from pathlib import Path
import shutil
import os
from ..config import constant
router = APIRouter()


# During startup delete the last session files and ChromaDB directories
@router.post("/removetempfiles")
async def cleanup_system():
    """Clean both temp files and all ChromaDB directories"""
    try:
        # 1. Clean upload temp files
        temp_files = [f for f in os.listdir() if f.startswith("temp_")]
        for temp_file in temp_files:
            os.remove(temp_file)
            print(f"Deleted temp file: {temp_file}")

        constant.global_state.temp_paths = []
            
        # 2. Clean all ChromaDB directories (with timestamp pattern)
        constant.global_state.vector_store = None
        
        # Find all chroma_db directories using the timestamp pattern
        chroma_dirs = [d for d in os.listdir() if d.startswith("chroma_db_")]
        
        if chroma_dirs:
            for chroma_dir in chroma_dirs:
                chroma_path = Path(f"./{chroma_dir}")
                if chroma_path.exists():
                    shutil.rmtree(chroma_path)
                    print(f"Deleted ChromaDB directory: {chroma_path}")
        else:
            print("No ChromaDB directories found")
            
        # Also check for the original chroma_db directory format
        legacy_chroma_path = Path("./chroma_db")
        if legacy_chroma_path.exists():
            shutil.rmtree(legacy_chroma_path)
            print(f"Deleted legacy ChromaDB directory: {legacy_chroma_path}")

        # Clear any stored path reference
        if hasattr(constant.global_state, "vector_store_path"):
            constant.global_state.vector_store_path = None

        return {"status": "Cleanup successful"}
        
    except Exception as e:
        raise HTTPException(500, f"Cleanup failed: {str(e)}")