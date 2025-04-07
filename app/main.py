# app/main.py
from fastapi import FastAPI  # Import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import the router
from app.api.endpoints.vector_search import router as vector_search_router

app = FastAPI()

# Set CORS policy (adjust origins to the specific Streamlit domain if in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vector_search_router, prefix="/api/v1")
