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


@app.route("/upload_zip", methods=["POST"])
def upload_zip():
    try:
        # Check if there are any files in the request
        if "audio_zip" not in request.files:
            logging.error("No zip file provided in the request")
            return jsonify(error="No zip file provided"), 400

        audio_zip = request.files["audio_zip"]
        if audio_zip.filename == "":
            logging.error("No selected file")
            return jsonify(error="No selected file"), 400

        # Create a temporary directory to extract audio files
        temp_directory = "temp"
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)

        # Generate a unique directory name
        unique_directory = str(uuid.uuid4())
        extract_directory = os.path.join(temp_directory, unique_directory)
        os.makedirs(extract_directory)

        # Save the zip file to the temporary directory
        zip_path = os.path.join(extract_directory, audio_zip.filename)
        audio_zip.save(zip_path)

        # Extract audio files from the zip archive
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_directory)

        # Call the main function for each extracted audio file
        transcriptions = {}
        for filename in os.listdir(extract_directory):
            if filename.endswith(".mp3"):  # Adjust file extension as needed
                audio_file_path = os.path.join(extract_directory, filename)
                transcription, location = main(audio_file_path)
                transcriptions[filename] = {
                    "transcription": transcription,
                    "location": location,
                }

        # Clean up temporary directory
        shutil.rmtree(extract_directory)

        # Log successful transcription
        logging.info("All files transcribed successfully")

        return jsonify(
            message="All files transcribed successfully", transcriptions=transcriptions
        )

    except Exception as e:
        # Log any exceptions that occur during the upload process
        logging.error("An error occurred during file upload: %s", e, exc_info=True)
        return jsonify(error="An error occurred during file upload"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# import requests

# # Define the URL for the Flask endpoint
# url = 'http://127.0.0.1:5000/upload'

# # Specify the path to the audio file you want to upload
# audio_file_path = '/content/diarization.mp3'  # Replace with the path to your audio file

# # Prepare the file data
# files = {
#     'audio': open(audio_file_path, 'rb')
# }


# # Send the POST request with the file data
# response = requests.post(url, files=files)

# # Print the response
# print(response.json())
