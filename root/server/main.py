from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import upload,ask,delete_tempfiles

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(delete_tempfiles.router)
