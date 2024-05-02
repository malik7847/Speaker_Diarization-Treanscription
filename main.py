from Utils import main
from flask import Flask, request, jsonify
import os


app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/upload", methods=["POST"])
def upload():
    # Check if there are any files in the request
    if "audio" not in request.files:
        return jsonify(error="No audio file provided"), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify(error="No selected file"), 400

    save_directory = "uploads"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Save the audio file to the directory
    file_path = os.path.join(save_directory, audio_file.filename)
    audio_file.save(file_path)
    x, y = main(file_path)

    return jsonify(message="File Transcribed successfully", Transcription=x, location=y)


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
