import httpx
import logging
from app.core.config import config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/fetch_content.log')  # Logs to console; replace with a FileHandler for file logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

async def fetch_content(ids, token: str):
    content_endpoint = config.get("content_service.retrieve_endpoint")
    content = []
    failed_ids = []  # To keep track of failed IDs
    headers = {
        'cognitoToken': token,
        'Content-Type': 'application/json',
    }

    async with httpx.AsyncClient() as client:
        for id in ids:
            try:
                response = await client.get(f"{content_endpoint}/{id}", headers=headers)
                if response.status_code == 200:
                    content.append(response.json())
                else:
                    failed_ids.append(id)
                    logger.warning(f"Failed to fetch content for ID {id}. Status code: {response.status_code}")
            except Exception as e:
                failed_ids.append(id)
                logger.error(f"Error fetching content for ID {id}: {str(e)}", exc_info=True)
    
    if failed_ids:
        logger.info(f"Failed IDs: {failed_ids}")  # Log the failed IDs for debugging
    
    return content
