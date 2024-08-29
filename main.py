import logging
from Utils import main
from flask import Flask, request, jsonify
import os
import shutil
import zipfile
import uuid

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/upload", methods=["POST"])
def upload():
    try:
        # Check if there are any files in the request
        if "audio" not in request.files:
            logging.error("No audio file provided in the request")
            return jsonify(error="No audio file provided"), 400

        audio_file = request.files["audio"]
        if audio_file.filename == "":
            logging.error("No selected file")
            return jsonify(error="No selected file"), 400

        save_directory = "uploads"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Save the audio file to the directory
        file_path = os.path.join(save_directory, audio_file.filename)
        audio_file.save(file_path)

        # Call the main function from Utils module
        x, y = main(file_path)

        # Log successful transcription
        logging.info("File transcribed successfully")

        return jsonify(
            message="File Transcribed successfully", Transcription=x, location=y
        )

    except Exception as e:
        # Log any exceptions that occur during the upload process
        logging.error("An error occurred during file upload: %s", e, exc_info=True)
        return jsonify(error="An error occurred during file upload"), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

