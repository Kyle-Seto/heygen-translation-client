import subprocess
import sys
import time
from client import VideoTranslationClient

def test_video_translation_flow():
    server_process = subprocess.Popen([sys.executable, "-m", "mock_server.app"])
    time.sleep(2)  # Give the server time to start
    
    # Run the test
    client = VideoTranslationClient()
    final_status = client.poll_until_complete()
    assert final_status["result"] in ["completed", "error"]
    
    # Clean up
    server_process.terminate()
    server_process.wait()
