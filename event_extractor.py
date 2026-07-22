import requests
import json
from config import LLAMA_SERVER

session = requests.Session()

EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["add", "query"]
        },
        "content": {"type": "string"},
        "date_phrase": {"type": "string"},
        "time_phrase": {"type": "string"}
    },
    "required": ["action", "content", "date_phrase", "time_phrase"]
}

EVENT_PROMPT = """
Extract calendar/event details from the user's message into a JSON object
with these fields:

- action: "add" (the user wants to note down a new event/appointment) or
  "query" (the user is asking what's on their calendar)
- content: a short description of the event (e.g. "dentist visit",
  "Ravi visiting"). Empty string for "query" actions.
- date_phrase: the raw date or date-range expression, copied as close as
  possible to how the user said it (e.g. "Monday", "next week", "this
  weekend", "the 14th", "next Tuesday"). Do NOT resolve this to an actual
  date yourself — just extract the phrase.
- time_phrase: the raw clock-time expression if one was given (e.g.
  "3 PM"), or an empty string if no specific time was mentioned. This
  should almost always be empty for "query" actions.

Never explain. Return only the JSON object.

Examples:

"Mark that I have a dentist visit on Monday"
{"action":"add","content":"dentist visit","date_phrase":"Monday","time_phrase":""}

"Put it in my calendar that Ravi is visiting on Tuesday at 3 PM"
{"action":"add","content":"Ravi visiting","date_phrase":"Tuesday","time_phrase":"3 PM"}

"I have a checkup coming up, note the date as the 14th"
{"action":"add","content":"checkup","date_phrase":"the 14th","time_phrase":""}

"What appointments do I have next week?"
{"action":"query","content":"","date_phrase":"next week","time_phrase":""}

"Am I free this Saturday?"
{"action":"query","content":"","date_phrase":"this Saturday","time_phrase":""}

"Do I have anything planned this weekend?"
{"action":"query","content":"","date_phrase":"this weekend","time_phrase":""}
"""


def extract_event(user_text):
    payload = {
        "messages": [
            {"role": "system", "content": EVENT_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0,
        "max_tokens": 100,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "event_schema",
                "schema": EVENT_SCHEMA
            }
        }
    }

    try:
        response = session.post(
            LLAMA_SERVER + "/v1/chat/completions",
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            print("Event Extractor Server Error:", response.status_code)
            print("Event Extractor Error Body:", response.text)
            return None

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        print("\n========== EVENT EXTRACT RAW ==========")
        print(repr(content))
        print("=========================================\n")

        return json.loads(content)

    except Exception as e:
        print("Event extraction error:", e)
        return None


def close_session():
    session.close()