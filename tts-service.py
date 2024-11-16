from flask import Flask, request, jsonify
from gtts import gTTS
import os
import hashlib
import re

app = Flask(__name__)

OUTPUT_DIR = "../shared_data/audio_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(text):
    """
    Generate a safe file name based on the text.
    """
    # Remove unsafe characters and truncate length
    text = re.sub(r'[^\w\s-]', '', text).strip()
    text = re.sub(r'[-\s]+', '_', text)
    return text[:50]  # Truncate to avoid excessively long file names


@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Create a user-friendly file name
        file_name = sanitize_filename(text) + ".mp3"
        output_file = os.path.join(OUTPUT_DIR, file_name)

        # Check if file already exists
        if os.path.exists(output_file):
            return jsonify({"message": "Audio already exists", "file_name": file_name}), 200

        # Generate and save the audio file
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)

        return jsonify({"message": "Audio generated", "file_name": file_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)