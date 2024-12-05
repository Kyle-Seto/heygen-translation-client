import requests
import time
import logging
from typing import Optional, TypedDict
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
    
    def poll_until_complete(
        self,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        max_retries: int = 20,
        timeout: Optional[float] = None
    ) -> StatusResponse:
        """
        Wait for job completion using exponential backoff.
        
        Args:
            initial_delay: Starting delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
            max_retries: Maximum number of retry attempts
            timeout: Maximum total time to wait in seconds
            
        Returns:
            Final status response
            
        Raises:
            ValueError: If initial_delay, max_delay, max_retries, or timeout is invalid
            VideoTranslationTimeout: If timeout is reached
            MaxRetriesExceeded: If max retries exceeded
            requests.exceptions.RequestException: On network/API errors
        """
        if initial_delay <= 0:
            raise ValueError("initial_delay must be positive")
        if max_delay < initial_delay:
            raise ValueError("max_delay must be >= initial_delay")
        if max_retries <= 0:
            raise ValueError("max_retries must be positive")
        if timeout is not None and timeout <= 0:
            raise ValueError("timeout must be positive or None")
            
        start_time = time.time()
        current_delay = initial_delay
        attempt = 1
        
        logger.info(
            f"Starting completion wait with exponential backoff "
            f"(initial_delay={initial_delay}s, max_delay={max_delay}s, "
            f"max_retries={max_retries}, timeout={timeout}s)"
        )
        
        while attempt <= max_retries:
            elapsed = time.time() - start_time
            
            if timeout and elapsed > timeout:
                logger.error(f"Timeout reached after {elapsed:.1f} seconds")
                raise
            
            logger.info(f"Attempt {attempt}/{max_retries}: Checking status")
            status = self.__get_status()
            result = status.get("result")
            
            if result in ["completed", "error"]:
                logger.info(f"Final status reached: {result}")
                return status
            
            if attempt == max_retries:
                logger.error(f"Max retries ({max_retries}) reached")
                raise
            
            # Calculate next delay with exponential backoff
            next_delay = min(current_delay * 2, max_delay)
            logger.info(
                f"Status still pending after {elapsed:.1f}s, "
                f"waiting {current_delay:.1f}s before next check "
                f"(next delay will be {next_delay:.1f}s)"
            )
            
            time.sleep(current_delay)
            current_delay = next_delay
            attempt += 1
