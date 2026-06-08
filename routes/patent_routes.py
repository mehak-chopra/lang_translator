from services.patent_service import (
    translate_citations,
    translate_npl_citations,
    translate_legal_events,
    TRANSLATABLE_FIELDS,
    TRANSLATABLE_LIST_FIELDS,
    translate_field,
    translate_list_field
)

from flask import jsonify
from app import app
import requests
from collections import OrderedDict
import os

from dotenv import load_dotenv

load_dotenv()

PATENT_API_BASE_URL = os.getenv(
    "PATENT_API_BASE_URL"
)


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

        forward_citations_translated = (
            translate_citations(
                patent_data.get(
                    "forward_citations_family",
                    []
                )   
            )
        )

        backward_citations_translated = (
            translate_citations(
                patent_data.get(
                    "backward_citations_family",
                    []
                )
            )
        )

        forward_citations_only_translated = (
            translate_citations(
                patent_data.get(
                    "forward_citations",
                    []
                )
            )
        )

        backward_citations_only_translated = (
            translate_citations(
                patent_data.get(
                    "backward_citations",
                    []
                )
            )
        )


        npl_citations_translated = (
            translate_npl_citations(
                patent_data.get(
                    "npl_citation",
                    []
                )
            )
        )

        legal_events_translated = (
            translate_legal_events(
                patent_data.get(
                    "legal_events",
                    []
                )
            )
        )

        response_data = OrderedDict()

        response_data["success"] = True

        response_data["patent_id"] = patent_id

        SPECIAL_FIELDS = {

            "legal_events":
                legal_events_translated,

            "forward_citations":
                forward_citations_only_translated,

            "forward_citations_family":
                forward_citations_translated,

            "backward_citations":
                backward_citations_only_translated,

            "backward_citations_family":
                backward_citations_translated,

            "npl_citation":
                npl_citations_translated
        }

        for key, value in patent_data.items():

            response_data[key] = value

            if key in TRANSLATABLE_FIELDS:

                response_data[
                    f"english_{key}"
                ] = translate_field(
                    value
                )

            elif key in TRANSLATABLE_LIST_FIELDS:

                response_data.update(

                    translate_list_field(
                        key,
                        value
                    )
                )

            elif key in SPECIAL_FIELDS:

                response_data[key] = (
                    SPECIAL_FIELDS[key]
                )

        return jsonify(response_data)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    