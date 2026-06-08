from services.translator_service import (
    translate_to_english
)

def translate_citations(citations):

    translated = []

    for citation in citations:

        assignee = citation.get(
            "assignee",
            ""
        )

        translated.append({

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

            "english_assignee":
                translate_to_english(
                    assignee
                )
        })

    return translated

from collections import OrderedDict

def translate_npl_citations(citations):

    translated = []

    for citation in citations:

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

        translated.append(
            translated_citation
        )

    return translated

def translate_legal_events(events):

    translated = []

    for event in events:

        description = event.get(
            "description"
        ) or {}

        owner_name = description.get(
            "owner_name",
            ""
        )

        translated.append({

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

    return translated