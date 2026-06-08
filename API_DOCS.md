# Language Translator & Patent Translation API

## Base URL

Local Development:

```text
http://127.0.0.1:5000
```

---

# 1. Translate Text

## Endpoint

```http
POST /api/translate
```

## Request Body

```json
{
  "text": "こんにちは"
}
```

## Success Response

```json
{
  "success": true,
  "data": {
    "detected_language": "Japanese (100.0% confidence)",
    "translated_text": "Hello",
    "warning_message": "",
    "info_message": ""
  }
}
```

## Error Response

```json
{
  "success": false,
  "error": "Please enter some text."
}
```

---

# 2. Patent Translation

## Endpoint

```http
GET /api/patent/<patent_id>
```

## Example

```http
GET /api/patent/JP4819386B2
```

## Sample Response

```json
{
  "success": true,
  "patent_id": "JP4819386B2",

  "title": "Measuring circuit and method...",
  "english_title": "Measuring circuit and method...",

  "applicant": "Samsung Electronics Co Ltd",
  "english_applicant": "Samsung Electronics Co Ltd",

  "inventors": [
    "時寧 崔"
  ],

  "english_inventors": [
    {
      "inventor": "時寧 崔",
      "inventor_english": "Shi Ning Cui"
    }
  ],

  "assignees": [
    "Samsung Electronics Co Ltd"
  ],

  "english_assignees": [
    {
      "assignee": "Samsung Electronics Co Ltd",
      "assignee_english": "Samsung Electronics Co Ltd"
    }
  ]
}
```

## Patent Translation Features

The endpoint preserves the original patent response while enriching it with English translations for:

* Patent title
* Applicant name
* Inventor names
* Assignee names
* NPL citation titles
* Forward citation assignees
* Backward citation assignees
* Citation family assignees
* Legal event owner names

Additional patent metadata is preserved from the original Wissen Research Patent API response.

## Error Response

```json
{
  "success": false,
  "error": "Patent not found."
}
```

---

# Features

### Language Translation

* Automatic language detection
* Translation to English
* Confidence score reporting
* Input validation
* Warning and information messages
* Error handling

### Patent Translation

* Patent metadata retrieval
* Patent title translation
* Applicant translation
* Inventor translation
* Assignee translation
* NPL citation title translation
* Forward citation translation
* Backward citation translation
* Citation family translation
* Legal event translation
* Preservation of original patent metadata

---

# Technologies Used

* Flask
* Python
* LangDetect
* Deep Translator (Google Translate)
* Requests
* JSON REST API

```
```
