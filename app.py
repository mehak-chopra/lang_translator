from flask import Flask, render_template, request, jsonify, send_file
from langdetect import detect_langs
from deep_translator import GoogleTranslator
from collections import OrderedDict
import requests
import re

from PyPDF2 import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

from dotenv import load_dotenv
import os

load_dotenv()

PATENT_API_BASE_URL = os.getenv(
    "PATENT_API_BASE_URL"
)

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
app.json.ensure_ascii = False

languages = {
    "hi": "Hindi",
    "ja": "Japanese",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "pa": "Punjabi",
    "ko": "Korean",
    "zh-cn": "Chinese",
    "en": "English",
    "ru": "Russian",
    "it": "Italian",
    "ar": "Arabic"
}

def translate_to_english(text):

    try:

        # First try normal auto detection
        english = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        # If translation failed or returned same text,
        # try Chinese transliteration as fallback
        if (
            not english or
            english.strip() == text.strip()
        ):

            english = GoogleTranslator(
                source="zh-CN",
                target="en"
            ).translate(text)

        return english

    except Exception:

        return text

def translate_list(items):

    translated_items = []

    for item in items:

        english = translate_to_english(item)

        translated_items.append({
            "assignee": item,
            "assignee_english": english if english else item
        })

    return translated_items

def process_translation_request(user_text):

    detected_language = ""
    translated_text = ""
    error_message = ""
    warning_message = ""
    info_message = ""

    try:

        # Empty or spaces only
        if not user_text.strip():

            error_message = "Please enter some text."

        # Numbers only
        elif user_text.strip().isdigit():

            error_message = (
                "Language cannot be detected from numbers only."
            )

        # Special characters only
        elif not re.search(
            r"[^\W\d_]",
            user_text,
            re.UNICODE
        ):

            error_message = (
                "Please enter meaningful text."
            )

        else:

            result = detect_langs(user_text)

            lang_code = result[0].lang
            confidence = result[0].prob * 100

            language_name = languages.get(
                lang_code,
                "Unknown Language"
            )

            warnings = []

            # Short text warning
            if len(user_text.split()) < 3:

                warnings.append(
                    "Text is very short. Language detection may not be accurate."
                )

            # Low confidence warning
            if confidence < 60:

                warnings.append(
                    "Language detection confidence is low. Results may not be accurate."
                )

            # Ambiguous detection warning
            if (
                len(result) > 1 and
                abs(result[0].prob - result[1].prob) < 0.15
            ):

                warnings.append(
                    "Language detection is ambiguous. Multiple languages are possible."
                )

            warning_message = " ".join(warnings)

            detected_language = (
                f"{language_name} "
                f"({confidence:.1f}% confidence)"
            )

            # Already English
            if lang_code == "en":

                info_message = (
                    "The text is already in English."
                )

                translated_text = user_text

            else:

                try:

                    translated_text = translate_to_english(user_text)

                    if not translated_text:

                        error_message = (
                            "Translation could not be generated."
                        )

                except Exception:

                    error_message = (
                        "This language is currently unsupported "
                        "or the translation service is unavailable."
                    )

    except Exception:

        error_message = (
            "An unexpected error occurred. "
            "Please try again."
        )

    return {
        "detected_language": detected_language,
        "translated_text": translated_text,
        "error_message": error_message,
        "warning_message": warning_message,
        "info_message": info_message
    }

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

@app.route("/api/patent/<patent_id>", methods=["GET"])
def patent_translate(patent_id):

    try:

        url = f"{PATENT_API_BASE_URL}/patent/{patent_id}"

        response = requests.get(url)

        if response.status_code != 200:

            return jsonify({
                "success": False,
                "error": "Patent not found."
            }), 404

        patent_data = response.json()

        inventors = patent_data.get(
            "inventors",
            []
        )

        assignees = patent_data.get(
            "assignees",
            []
        )

        forward_citations_translated = []
        backward_citations_translated = []

        forward_citations_only_translated = []
        backward_citations_only_translated = []

        npl_citations_translated = []

        legal_events_translated = []

        # Forward family citations
        for citation in patent_data.get(
            "forward_citations_family",
            []
        ):

            assignee = citation.get(
                "assignee",
                ""
            )

            forward_citations_translated.append({

                "patent_number": citation.get(
                    "patent_number"
                ),

                "priority_date": citation.get(
                    "priority_date"
                ),

                "pub_date": citation.get(
                    "pub_date"
                ),

                "examiner_cited": citation.get(
                    "examiner_cited"
                ),

                "assignee": assignee,

                "english_assignee": translate_to_english(
                    assignee
                )
            })

        # Backward family citations
        for citation in patent_data.get(
            "backward_citations_family",
            []
        ):

            assignee = citation.get(
                "assignee",
                ""
            )

            backward_citations_translated.append({

                "patent_number": citation.get(
                    "patent_number"
                ),

                "priority_date": citation.get(
                    "priority_date"
                ),

                "pub_date": citation.get(
                    "pub_date"
                ),

                "examiner_cited": citation.get(
                    "examiner_cited"
                ),

                "assignee": assignee,

                "english_assignee": translate_to_english(
                    assignee
                )
            })

        # Forward citations only
        for citation in patent_data.get(
            "forward_citations",
            []
        ):

            assignee = citation.get(
                "assignee",
                ""
            )

            forward_citations_only_translated.append({

                "patent_number": citation.get(
                    "patent_number"
                ),

                "priority_date": citation.get(
                    "priority_date"
                ),

                "pub_date": citation.get(
                    "pub_date"
                ),

                "examiner_cited": citation.get(
                    "examiner_cited"
                ),

                "assignee": assignee,

                "english_assignee": translate_to_english(
                    assignee
                )
            })

        # Backward citations only
        for citation in patent_data.get(
            "backward_citations",
            []
        ):

            assignee = citation.get(
                "assignee",
                ""
            )

            backward_citations_only_translated.append({

                "patent_number": citation.get(
                    "patent_number"
                ),

                "priority_date": citation.get(
                    "priority_date"
                ),

                "pub_date": citation.get(
                    "pub_date"
                ),

                "examiner_cited": citation.get(
                    "examiner_cited"
                ),

                "assignee": assignee,

                "english_assignee": translate_to_english(
                    assignee
                )
            })

        # NPL citations
        for citation in patent_data.get(
            "npl_citation",
            []
        ):

            title = citation.get(
                "title",
                ""
            )

            translated_citation = OrderedDict()

            translated_citation["title"] = title

            translated_citation["english_title"] = (
                translate_to_english(title)
                if title else ""
            )

            translated_citation["cited_by_examiner"] = (
                citation.get(
                    "cited_by_examiner"
                )
            )   

            translated_citation["cited_by_third_party"] = (
                citation.get(
                    "cited_by_third_party"
                )
            )

            npl_citations_translated.append(
                translated_citation
            )   

        # Legal events
        for event in patent_data.get(
            "legal_events",
            []
        ):

            description = event.get(
                "description"
            ) or {}

            owner_name = description.get(
                "owner_name",
                ""
            )

            legal_events_translated.append({

                "date": event.get(
                    "date"
                ),

                "code": event.get(
                    "code"
                ),

                "title": event.get(
                    "title"
                ),

                "description": {

                    "owner_name": owner_name,

                    "owner_name_english":
                        translate_to_english(
                            owner_name
                        ) if owner_name else "",

                    "free_format_text":
                        description.get(
                            "free_format_text"
                        ),

                    "effective_date":
                        description.get(
                            "effective_date"
                        )
                }
            })


        response_data = OrderedDict()

        response_data["success"] = True

        response_data["patent_id"] = patent_id

        for key, value in patent_data.items():

            response_data[key] = value

            if key == "title":

                response_data["english_title"] = (
                    translate_to_english(
                        value or ""
                    )
                )


            elif key == "assignees":

                response_data["english_assignees"] = (
                    translate_list(
                        assignees
                    )
                )

            elif key == "inventors":

                response_data["english_inventors"] = [
                    {
                        "inventor": inventor,
                        "inventor_english": 
                            translate_to_english(
                                inventor
                            )
                    }
                    for inventor in inventors
                ]

            elif key == "applicant":

                response_data["english_applicant"] = (
                    translate_to_english(
                        value or ""
                    )
                )

            elif key == "legal_events":

                response_data["legal_events"] = (
                    legal_events_translated
                )

            elif key == "forward_citations":

                response_data["forward_citations"] = (
                    forward_citations_only_translated
                )

            elif key == "forward_citations_family":

                response_data["forward_citations_family"] = (
                    forward_citations_translated
                )

            elif key == "backward_citations":

                response_data["backward_citations"] = (
                    backward_citations_only_translated
                )

            elif key == "backward_citations_family":

                response_data["backward_citations_family"] = (
                    backward_citations_translated
                )

            elif key == "npl_citation":

                response_data["npl_citation"] = (
                    npl_citations_translated
                )

        return jsonify(response_data)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
if __name__ == "__main__":
    app.run(debug=True)