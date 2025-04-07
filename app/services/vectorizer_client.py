# app/services/vectorizer_client.py
import base64
import io
import httpx
from PIL import Image
from app.core.config import config

async def vectorize_text(text: str):
    text_endpoint = config.get("vectorizer_service.text_endpoint")
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(text_endpoint, json={"text": text})
        response.raise_for_status()
    return response.json()["embedding"]

async def vectorize_image(base64_image_str):
    # Decode the base64 image string
    image_data = base64.b64decode(base64_image_str)
    
    # Convert to a PIL Image
    image = Image.open(io.BytesIO(image_data))
    
    # Save the image to a BytesIO object in a format like PNG or JPEG
    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    image_file.seek(0)  # Move to the beginning of the file
    
    # Prepare the endpoint and payload for httpx
    image_endpoint = config.get("vectorizer_service.image_endpoint")
    async with httpx.AsyncClient(verify=False) as client:
        files = {"file": ("image.png", image_file, "image/png")}
        response = await client.post(image_endpoint, files=files, timeout=80.0)
        response.raise_for_status()
    
    return response.json()["embedding"]
