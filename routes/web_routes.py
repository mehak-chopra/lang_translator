from flask import render_template, request
from app import app
from services.translator_service import (
    process_translation_request
)

@app.route("/", methods=["GET", "POST"])
def home():

    user_text = ""

    result = {
        "detected_language": "",
        "translated_text": "",
        "error_message": "",
        "warning_message": "",
        "info_message": ""
    }

    if request.method == "POST":

        user_text = request.form.get("text", "")

        result = process_translation_request(user_text)

    return render_template(
        "index.html",
        detected_language=result["detected_language"],
        translated_text=result["translated_text"],
        user_text=user_text,
        error_message=result["error_message"],
        warning_message=result["warning_message"],
        info_message=result["info_message"]
    )