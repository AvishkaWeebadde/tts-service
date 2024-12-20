from flask import Flask, request, jsonify
from gtts import gTTS
import os
import re
from pydub import AudioSegment

app = Flask(__name__)

OUTPUT_DIR = "../shared_data/audio_files2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COMBINED_DIR = "../shared_data/combined_audio"
os.makedirs(COMBINED_DIR, exist_ok=True)

def sanitize_filename(text):
    text = re.sub(r'[^\w\s-]', '', text).strip()
    text = re.sub(r'[-\s]+', '_', text)
    return text[:50]

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text_chunks = data.get('text', [])
    if not text_chunks:
        return jsonify({"error": "No text provided"}), 400

    responses = []
    for text in text_chunks:
        try:
            file_name = sanitize_filename(text) + ".mp3"
            output_file = os.path.join(OUTPUT_DIR, file_name)

            if os.path.exists(output_file):
                responses.append({"message": "Audio already exists", "file_name": file_name})
                continue

            tts = gTTS(text=text, lang='en')
            tts.save(output_file)
            responses.append({"message": "Audio generated", "file_name": file_name})
        except Exception as e:
            responses.append({"error": str(e)})

    return jsonify({"file_paths": [response["file_name"] for response in responses if "file_name" in response]}), 200


@app.route('/combine', methods=['POST'])
def combine_audio():
    data = request.json
    file_paths = data.get('file_paths', [])

    if not file_paths:
        return jsonify({"error": "No file paths provided"}), 400

    try:
        combined_audio = AudioSegment.empty()
        for file_path in file_paths:
            audio_file = os.path.join(OUTPUT_DIR, file_path)
            if not os.path.exists(audio_file):
                return jsonify({"error": f"File not found: {file_path}"}), 404
            combined_audio += AudioSegment.from_file(audio_file)

        combined_file_name = "combined_audio.mp3"
        combined_file_path = os.path.join(COMBINED_DIR, combined_file_name)
        combined_audio.export(combined_file_path, format="mp3")

        return jsonify({"message": "Audio files combined successfully", "file_path": combined_file_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)