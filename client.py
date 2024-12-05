import requests
import logging
from typing import TypedDict
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 5 seconds for all status requests
GET_STATUS_TIMEOUT = 5

class StatusResponse(TypedDict):
    """Type definition for status response."""
    result: str  # 'pending' | 'completed' | 'error'

class VideoTranslationClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        # Validate URL format
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid base URL: {base_url}")
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        logger.info(f"Initialized client with base URL: {base_url}")

    def __get_status(self) -> StatusResponse:
        try:
            logger.info(f"Requesting status from {self.base_url}/status")
            response = self.session.get(f"{self.base_url}/status", timeout=GET_STATUS_TIMEOUT)
            status: StatusResponse = response.json()
            logger.info(f"Received status: {status}")
            return status
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out after {GET_STATUS_TIMEOUT}s")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get status: {str(e)}")
            raise
