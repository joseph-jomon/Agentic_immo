# app/services/database_client.py
import httpx
from app.core.config import config

async def text_search_database(vector: list, index_name: str):
    # Endpoint and query parameter setup
    search_endpoint = config.get("database_service.text_search_endpoint")
    url = f"{search_endpoint}/{index_name}"
    
    # Prepare the payload in the required format
    payload = {"search_vector": vector}

    # Perform the search request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            params={"index_name": index_name},  # Query parameter for index name
            json=payload  # JSON payload
        )
        
        # Check if the response is successful
        if response.status_code == 200:
            # Extracting IDs from the response JSON
            response_data = response.json()
            # Accessing hits within the response
            hits = response_data.get("hits", [])
            # Extract all _id values from hits
            search_ids = [hit.get("_id") for hit in hits if "_id" in hit]
            

            
            return search_ids
        else:
            raise Exception(f"Failed to execute search: {response.text}")

async def image_search_database(vector: list, index_name: str):
    # Endpoint and query parameter setup
    search_endpoint = config.get("database_service.image_search_endpoint")
    url = f"{search_endpoint}/{index_name}"
    
    # Prepare the payload in the required format
    payload = {"search_vector": vector}

    # Perform the search request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            params={"index_name": index_name},  # Query parameter for index name
            json=payload  # JSON payload
        )
        
        # Check if the response is successful
        if response.status_code == 200:
            # Extracting IDs from the response JSON
            response_data = response.json()
            # Accessing hits within the response
            hits = response_data.get("hits", [])
            # Extract all _id values from hits
            search_ids = [hit.get("_source").get('id') for hit in hits if "id" in hit.get('_source')]
            

            
            return search_ids
        else:
            raise Exception(f"Failed to execute search: {response.text}")

async def combined_search_database(vector: list, text_index_name: str, image_index_name: str):
    # Endpoint and query parameter setup
    search_endpoint = config.get("database_service.combined_search_endpoint")
    url = f"{search_endpoint}"

    # Prepare the payload in the required format
    payload = {"search_vector": vector}

    # Perform the search request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            params={"text_index_name": text_index_name, "image_index_name": image_index_name},  # Query parameters for index names
            json=payload  # JSON payload
        )
        
        # Check if the response is successful
        if response.status_code == 200:
            # Extracting IDs from the response JSON
            response_data = response.json()
            # Accessing hits within the response
            hits = response_data.get("hits", [])
            # Extract all _id values from hits
            search_ids = [hit.get("source").get('id') for hit in hits if "id" in hit.get('source')]
            
            return search_ids
        else:
            raise Exception(f"Failed to execute search: {response.text}")
