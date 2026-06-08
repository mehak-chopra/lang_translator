from services.patent_service import (
    translate_citations
)
from services.patent_service import (
    translate_citations,
    translate_npl_citations
)
from services.patent_service import (
    translate_citations,
    translate_npl_citations,
    translate_legal_events
)

from flask import jsonify
from app import app
import requests
from collections import OrderedDict
import os

from services.translator_service import (
    translate_to_english,
    translate_list
)

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
    