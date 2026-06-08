from flask import request, jsonify
from app import app
from services.translator_service import (
    process_translation_request
)

@app.route("/api/translate", methods=["POST"])
def api_translate():

    data = request.get_json()

    user_text = data.get("text", "")

    result = process_translation_request(user_text)

    if result["error_message"]:

        return jsonify({
            "success": False,
            "error": result["error_message"]
        }), 400

    return jsonify({
        "success": True,
        "data": {
            "detected_language": result["detected_language"],
            "translated_text": result["translated_text"]
        },
        "warning": result["warning_message"],
        "info": result["info_message"]
    })