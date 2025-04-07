# app/core/dependencies.py
import httpx
from fastapi import Depends, HTTPException, Request
from app.services.vectorizer_client import vectorize_text, vectorize_image
from app.api.schemas import VectorSearchRequest  # Updated import
from app.core.config import config

async def get_vector(request: VectorSearchRequest):
    if request.text:
        return await vectorize_text(request.text)
    elif request.image:
        return await vectorize_image(request.image)
    else:
        raise HTTPException(status_code=400, detail="Invalid input: text or image required")

async def authenticate_api_key():

    API_KEY = "c89fbbe2-2f72-4464-913e-99b3bf7b5140"
    auth_url = "https://api.production.cloudios.flowfact-prod.cloud/admin-token-service/public/adminUser/authenticate"
    headers = {'token': API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(auth_url, headers=headers)

    if response.status_code == 200:
        token = response.text
        return token
    else:
        raise HTTPException(status_code=400, detail="Invalid API key")
