from fastapi import File, UploadFile, BackgroundTasks, HTTPException, APIRouter
from typing import List
import os
from ..config import constant
from ..services import file_processor

router = APIRouter()

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """Handle multi-format file upload"""
    try:
        temp_paths = constant.global_state.temp_paths
        for file in files:
            # Validate file extension
            ext = os.path.splitext(file.filename)[-1].lower()
            if ext not in constant.global_state.accepted_extensions:
                raise HTTPException(400, f"Unsupported file type: {ext}")
            
            # Save file
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            temp_paths.append(temp_path)
        
        if background_tasks:
            file_processor.process_files(temp_paths)
            return {"status": "Processing complete"}
        
        raise HTTPException(500, "Background tasks not available")
    
    except Exception as e:
        # Cleanup on error
        for path in temp_paths:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(500, f"Upload failed: {str(e)}")