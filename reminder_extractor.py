import requests
import json
from config import LLAMA_SERVER

# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------
session = requests.Session()

# ----------------------------------------
# Schema — LLM extracts structure only.
# time_phrase stays as raw text; Python (dateparser) resolves the
# actual datetime. This avoids asking the LLM to do date arithmetic,
# which we've already seen it get wrong (e.g. "years left until 2029").
# ----------------------------------------
REMINDER_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {"type": "string"},
        "time_phrase": {"type": "string"},
        "recurrence": {
            "type": "string",
            "enum": ["none", "daily", "weekly", "monthly", "yearly"]
        }
    },
    "required": ["content", "time_phrase", "recurrence"]
}

REMINDER_PROMPT = """
Extract reminder details from the user's message into a JSON object with
these fields:

- content: what the user wants to be reminded about. A short phrase,
  without "remind me to" / "set a reminder to" prefixes.
- time_phrase: the raw natural-language time/date expression, copied
  as close as possible to how the user said it (e.g. "tomorrow morning",
  "8 PM", "next Tuesday", "in two hours"). Do NOT resolve this to an
  actual date or do any date math yourself — just extract the phrase.
- recurrence: "none" | "daily" | "weekly" | "monthly" | "yearly".
  Use "daily" for "every day"/"every evening"/"every morning" style
  phrasing, "weekly" for "every week"/"every Monday", etc.
  Default to "none" if the reminder is one-time.

IMPORTANT: phrases like "next month", "next week", "next Monday", or
"next year" describe a SINGLE one-time occurrence, not repetition —
these must always get recurrence "none". Only use a non-"none" value
when the message explicitly signals repetition with words like
"every", "each", "daily", "weekly", "monthly", "yearly", "again and
again", etc.

Never explain. Return only the JSON object.

Examples:

"Remind me to take my tablets at 8 PM"
{"content":"take tablets","time_phrase":"8 PM","recurrence":"none"}

"Set a reminder to call my daughter tomorrow morning"
{"content":"call my daughter","time_phrase":"tomorrow morning","recurrence":"none"}

"I need to remember to water the plants every evening"
{"content":"water the plants","time_phrase":"evening","recurrence":"daily"}

"Nudge me before my grandson's birthday next month"
{"content":"grandson's birthday","time_phrase":"next month","recurrence":"none"}

"Make sure I don't miss my physiotherapy session every Monday"
{"content":"physiotherapy session","time_phrase":"Monday","recurrence":"weekly"}

"Remind me to pay the rent next month"
{"content":"pay the rent","time_phrase":"next month","recurrence":"none"}
"""


def extract_reminder(user_text):
    payload = {
        "messages": [
            {"role": "system", "content": REMINDER_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0,
        "max_tokens": 80,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "reminder_schema",
                "schema": REMINDER_SCHEMA
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
            print("Reminder Extractor Server Error:", response.status_code)
            print("Reminder Extractor Error Body:", response.text)
            return None

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        print("\n========== REMINDER EXTRACT RAW ==========")
        print(repr(content))
        print("===========================================\n")

        return json.loads(content)

    except Exception as e:
        print("Reminder extraction error:", e)
        return None


# ----------------------------------------
# Close Session
# ----------------------------------------
def close_session():
    session.close()