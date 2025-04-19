from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import upload,ask

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
