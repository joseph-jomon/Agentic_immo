# app/api/schemas.py
from pydantic import BaseModel
from typing import List

class VectorSearchRequest(BaseModel):
    text: str = None
    image: str = None

class VectorSearchResponse(BaseModel):
    ids: List[str]
    content: List[dict]
