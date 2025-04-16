from flask import Flask, request, jsonify
from flask_cors import CORS
from music_utils import analyze_musicxml
from generate_utils import generate_melody

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

    if task == "analyzeMusic":
        result = analyze_musicxml(melody)
        return jsonify(result)

    elif task == "generateMelody":
        musicxml = generate_melody(style, key, time_sig, measures)
        return jsonify({
            "result": "Melody generated successfully",
            "musicXML": musicxml
        })

    return jsonify({"error": "Invalid task"}), 400

@app.route("/")
def home():
    return jsonify({"message": "Music Toolkit API is running."})
