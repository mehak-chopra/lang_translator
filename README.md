# Language Translator & Patent Translation API

A Flask-based application that provides language detection, text translation, and patent metadata translation services.

## Features

### Language Translation

* Automatic language detection
* Translation of text into English
* Confidence score reporting
* Input validation and error handling
* Warning messages for short or ambiguous text
* REST API support

### Patent Translation

* Patent information retrieval from the Wissen Research Patent API
* Translation of patent titles into English
* Translation of applicant names into English
* Translation of inventor names into English
* Translation of assignee names into English
* Translation of NPL (Non-Patent Literature) citation titles into English
* Translation of assignee names in forward citations
* Translation of assignee names in backward citations
* Translation of assignee names in citation family records
* Translation of legal event description fields (when applicable)
* Preservation of original patent metadata
* Enriched responses with translated English equivalents
* Translation of forward citation assignee lists
* Translation of patent citation assignees while preserving original metadata
* Generic field translation framework
* Generic list translation framework
* Environment variable configuration for external patent API integration
* Service-based translation architecture

## API Endpoints

### Translate Text

**POST** `/api/translate`

Request:

```json
{
  "text": "こんにちは"
}
```

### Patent Translation

**GET** `/api/patent/<patent_id>`

Example:

```http
GET /api/patent/JP4819386B2
```

Returns:

* Original patent metadata
* English translations of relevant names and titles
* Translated citation information
* Translated legal event information

## Project Structure

```text
lang-translator/
│
├── app.py
│
├── routes/
│   ├── web_routes.py
│   ├── translate_routes.py
│   └── patent_routes.py
│
├── services/
│   ├── translator_service.py
│   └── patent_service.py
│
├── templates/
├── static/
├── .env
├── requirements.txt
├── README.md
└── API_DOCS.md
```
## Architecture

The application follows a route-service architecture:

* Routes handle HTTP requests and responses.
* Services contain translation and patent-processing logic.
* Environment variables are used for external API configuration.
* Translation behavior is driven through reusable translation mappings for easier future expansion.

## Technologies Used

* Flask
* LangDetect
* Deep Translator (Google Translate)
* Requests
* Python

## Future Enhancements

* PDF to English PDF translation endpoint
* Public cloud deployment
* API documentation improvements
* Additional patent metadata translation support
