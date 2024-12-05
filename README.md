# HeyGen Video Translation Client Library

A Python client library for seamlessly interacting with HeyGen's video translation service. This library provides a simple interface to translate videos using HeyGen's AI-powered translation capabilities.

## Installation

```bash
# Clone the repository
git clone https://github.com/Kyle-Seto/heygen-translation-client.git
cd heygen-video-translation-client

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from client import VideoTranslationClient

# Initialize client (defaults to http://localhost:5000 if no URL provided)
client = VideoTranslationClient()

# Wait for completion with exponential backoff
final_status = client.poll_until_complete(
    initial_delay=1.0,    # Start with 1 second delay
    max_delay=30.0,       # Never wait more than 30 seconds between retries
    max_retries=20,       # Try up to 20 times
    timeout=300.0         # Give up after 5 minutes
)
print(f"Final status: {final_status}")
```

### Configuration Options

#### Client Configuration
- `base_url`: API endpoint URL for the video translation service
- `initial_delay`: Time between first retry when using poll_until_complete (in seconds)
- `max_delay`: Maximum wait time between status checks (in seconds)
- `max_retries`: Maximum number of retries
- `timeout`: Maximum time to wait for completion (in seconds, None for no timeout)

#### Mock Server Configuration
> Note: These configurations are only for the included mock server used for testing. They are not part of the client library and won't affect the actual HeyGen API integration.

- `base_processing_time`: Base time to simulate video processing (default: 30.0 seconds)
- `processing_time_noise`: Random variation in processing time (±seconds, default: 5.0)
- `error_probability`: Probability of simulated translation error (0.0 to 1.0, default: 0.2)

For example, the mock server with `base_processing_time=30.0` and `processing_time_noise=5.0` will simulate processing times between 25-35 seconds.

## Error Handling

The client provides several custom exceptions for better error handling:

#### ValueError: "Invalid base URL"
- **Cause**: The provided URL is missing a scheme (http/https) or host
- **Solution**: Ensure the URL includes both protocol and host, e.g., `http://localhost:5000` or `https://api.heygen.com`

#### VideoTranslationTimeout
- **Cause**: Operation took longer than the specified timeout duration
- **Solution**: 
  - Increase the `timeout` parameter in `poll_until_complete`
  - Check server load or network connectivity
  - If using mock server, consider increasing `base_processing_time`

#### MaxRetriesExceeded
- **Cause**: Server didn't return a final status within the maximum number of retry attempts
- **Solution**:
  - Increase `max_retries` parameter
  - Adjust retry timing with `initial_delay` and `max_delay`
  - Check server logs for potential processing issues

#### Network Request Failed
- **Cause**: Connection issues between client and server
- **Solution**:
  - Verify the server is running and accessible
  - Check network connectivity
  - Ensure firewall settings allow the connection
  - Verify the port is correct in the base URL
