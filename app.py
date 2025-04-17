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
    pitch_pool = data.get("pitchPool")

    if task == "analyzeMusic":
        try:
            result = analyze_musicxml(melody)
            return jsonify({
                "status": "success",
                "message": "分析成功",
                "analysisResult": result
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"音樂分析失敗：{str(e)}"
            }), 500

    elif task == "generateMelody":
        try:
            musicxml_result = generate_melody(style, key, time_sig, measures, pitch_pool)

            if isinstance(musicxml_result, dict) and "error" in musicxml_result:
                return jsonify({
                    "status": "error",
                    "message": musicxml_result["error"]
                }), 400

            return jsonify({
                "status": "success",
                "message": "旋律生成成功",
                "keyUsed": key,
                "musicXMLUrl": str(musicxml_result)
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"伺服器錯誤：{str(e)}"
            }), 500

    else:
        return jsonify({
            "status": "error",
            "message": "無效的任務參數（task）"
        }), 400

@app.route("/")
def home():
    return jsonify({"message": "Music Toolkit API is running."})
