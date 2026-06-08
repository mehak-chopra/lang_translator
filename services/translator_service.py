from langdetect import detect_langs
from deep_translator import GoogleTranslator
import re

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
        english = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

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