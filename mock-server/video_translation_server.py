import time
import random
from video_translation_types import StatusResponse

class VideoTranslationServer:
    def __init__(
        self, 
        base_processing_time: float = 30.0,
        processing_time_noise: float = 5.0,
        error_probability: float = 0.2
    ):
        self.start_time = time.time()
        self.base_processing_time = base_processing_time
        self.processing_time_noise = processing_time_noise
        self.error_probability = error_probability
        self.actual_processing_time = base_processing_time + random.uniform(
            -processing_time_noise, 
            processing_time_noise
        )
    
    @property
    def status(self) -> StatusResponse:
        """Automatically calculate current status based on elapsed time."""
        elapsed = time.time() - self.start_time
        if elapsed >= self.actual_processing_time:
            if random.random() < self.error_probability:
                return {"result": "error"}
            return {"result": "completed"}
        return {"result": "pending"}