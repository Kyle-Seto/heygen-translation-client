from flask import Flask, jsonify
from .video_translation_server import VideoTranslationServer

app = Flask(__name__)

BASE_PROCESSING_TIME = 30.0  # Base time to process a video
PROCESSING_TIME_NOISE = 5.0  # Random variation in processing time (+/-)
ERROR_PROBABILITY = 0.2      # Probability of translation error

server = VideoTranslationServer(
    base_processing_time=BASE_PROCESSING_TIME,
    processing_time_noise=PROCESSING_TIME_NOISE,
    error_probability=ERROR_PROBABILITY
)

@app.route("/status")
def get_status():
    return jsonify(server.status())

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
