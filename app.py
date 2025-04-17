from flask import Flask, request, jsonify
from flask_cors import CORS
from music_utils import analyze_musicxml
from melody_generator import generate_melody

import os

app = Flask(__name__)
CORS(app)

# ✅ 防止中文亂碼（可選）
app.config['JSON_AS_ASCII'] = False

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
                "message": "Analysis completed.",
                "analysisResult": result
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Music analysis failed: {str(e)}"
            }), 500

    elif task == "generateMelody":
        try:
            musicxml_result = generate_melody(style, key, time_sig, measures, pitch_pool)

            # ✅ 如果是錯誤訊息，回傳 error 狀態
            if isinstance(musicxml_result, dict) and "error" in musicxml_result:
                return jsonify({
                    "status": "error",
                    "message": musicxml_result["error"]
                }), 400

            # ✅ 正確情況，回傳 GPT 友善格式
            return jsonify({
                "status": "success",
                "message": "Melody generated successfully.",
                "keyUsed": key,
                "musicXMLUrl": str(musicxml_result)
            })

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }), 500

    else:
        return jsonify({
            "status": "error",
            "message": "Invalid task type."
        }), 400

# ✅ 加上根目錄測試（可選）
@app.route("/")
def home():
    return jsonify({
        "message": "🎵 Music Toolkit API is running.",
        "status": "online"
    })

# ✅ 啟動 Flask server（Render 用）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
