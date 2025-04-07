# app/api/endpoints/vector_search.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import VectorSearchRequest, VectorSearchResponse  # Updated imports
from app.core.dependencies import get_vector, authenticate_api_key
from app.services.database_client import text_search_database, image_search_database ,combined_search_database
from app.services.content_client import fetch_content

router = APIRouter()

@router.post("/text_vector_search", response_model=VectorSearchResponse)
async def text_vector_search(
    request: VectorSearchRequest,
    vector: list = Depends(get_vector),
    token: str = Depends(authenticate_api_key)
):
    # Search in the database with the given vector
    search_ids = await text_search_database(vector, index_name="text_kawohls")
    if not search_ids:
        return VectorSearchResponse(ids=[], content=[])

    # Use the token to fetch content for each search ID
    content = await fetch_content(search_ids, token=token)

    return VectorSearchResponse(ids=search_ids, content=content)

@router.post("/image_vector_search", response_model=VectorSearchResponse)
async def image_vector_search(
    request: VectorSearchRequest,
    vector: list = Depends(get_vector),
    token: str = Depends(authenticate_api_key)
):
    # Search in the database with the given vector
    search_ids = await image_search_database(vector, index_name="image_kawohls")
    if not search_ids:
        return VectorSearchResponse(ids=[], content=[])

    # Use the token to fetch content for each search ID
    content = await fetch_content(search_ids, token=token)

    return VectorSearchResponse(ids=search_ids, content=content)

@router.post("/combined_vector_search", response_model=VectorSearchResponse)
async def text_vector_search(
    request: VectorSearchRequest,
    vector: list = Depends(get_vector),
    token: str = Depends(authenticate_api_key)
):
    # Search in the database with the given vector
    search_ids = await combined_search_database(vector, text_index_name="text_kawohls", image_index_name="image_kawohls")
    if not search_ids:
        return VectorSearchResponse(ids=[], content=[])

    # Use the token to fetch content for each search ID
    content = await fetch_content(search_ids, token=token)

    return VectorSearchResponse(ids=search_ids, content=content)