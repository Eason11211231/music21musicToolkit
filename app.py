from flask import Flask, request, jsonify
from flask_cors import CORS
from music_utils import analyze_musicxml
from melody_generator import generate_melody

app = Flask(__name__)
CORS(app)

@app.route("/musicToolkit", methods=["POST"])
def handleMusicTask():
    data = request.get_json()
    task = data.get("task")
    style = data.get("style")
    key = data.get("key")
    time_sig = data.get("timeSignature")
    melody = data.get("melody")
    measures = data.get("measures", 8)
    pitch_pool = data.get("pitchPool")  # ✅ 正確放在這裡

    if task == "analyzeMusic":
        result = analyze_musicxml(melody)
        return jsonify(result)

    elif task == "generateMelody":
        musicxml_path = generate_melody(style, key, time_sig, measures, pitch_pool)
        return jsonify({
            "result": "Melody generated successfully",
            "musicXML": str(musicxml_path)
        })

    else:
        return jsonify({"error": "Invalid task"}), 400

@app.route("/")
def home():
    return jsonify({"message": "Music Toolkit API is running."})
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
