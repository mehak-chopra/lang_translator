from flask import Flask, render_template, request, jsonify, send_file
from langdetect import detect_langs
from deep_translator import GoogleTranslator
import re

from PyPDF2 import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
app.json.ensure_ascii = False

from services.translator_service import (
    translate_to_english,
    translate_list,
    process_translation_request
)

from routes.web_routes import *
from routes.translate_routes import *
from routes.patent_routes import *

if __name__ == "__main__":
    app.run(debug=True)