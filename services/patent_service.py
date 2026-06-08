from collections import OrderedDict
from services.translator_service import (
    translate_to_english
)

TRANSLATABLE_FIELDS = [
    "title",
    "applicant"
]

TRANSLATABLE_LIST_FIELDS = [
    "inventors",
    "assignees",
    "forward_citation_assignees"
]

def translate_citations(citations):

    translated = []

    for citation in citations:

        translated_citation = dict(
            citation
        )

        assignee = citation.get(
            "assignee",
            ""
        )

        translated_citation[
            "english_assignee"
        ] = translate_to_english(
            assignee
        )

        translated.append(
            translated_citation
        )

    return translated

def translate_npl_citations(citations):

    translated = []

    for citation in citations:

        title = citation.get(
            "title",
            ""
        )

        translated_citation = OrderedDict()

        for key, value in citation.items():

            translated_citation[key] = value

            if key == "title":

                translated_citation[
                    "english_title"
                ] = (
                    translate_to_english(
                        title
                    )
                    if title else ""
                )

        translated.append(
            translated_citation
        )

    return translated

def translate_legal_events(events):

    translated = []

    for event in events:

        translated_event = dict(
            event
        )

        description = event.get(
            "description"
        ) or {}

        translated_description = OrderedDict()

        for key, value in description.items():

            translated_description[key] = value

            if key == "owner_name":

                translated_description[
                    "owner_name_english"
                ] = (
                    translate_to_english(
                        value
                    )
                    if value else ""
                )

        translated_event[
            "description"
        ] = translated_description

        translated.append(
            translated_event
        )

    return translated

def translate_field(value):

    return translate_to_english(
        value or ""
    )

def translate_inventors(inventors):

    return [
        {
            "inventor": inventor,
            "inventor_english":
                translate_to_english(
                    inventor
                )
        }
        for inventor in inventors
    ]

def translate_assignees(assignees):

    return [
        {
            "assignee": assignee,

            "assignee_english":
                translate_to_english(
                    assignee
                )
        }

        for assignee in assignees
    ]

LIST_TRANSLATORS = {

    "inventors": (
        "english_inventors",
        translate_inventors
    ),

    "assignees": (
        "english_assignees",
        translate_assignees
    ),

    "forward_citation_assignees": (
        "english_forward_citation_assignees",
        translate_assignees
    )
}

def translate_list_field(
    field_name,
    items
):

    if field_name not in LIST_TRANSLATORS:

        return {}

    output_key, translator = (
        LIST_TRANSLATORS[
            field_name
        ]
    )

    return {
        output_key:
            translator(items)
    }