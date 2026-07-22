import requests
import json
from config import LLAMA_SERVER

# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------
session = requests.Session()

SHOPPING_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["add", "remove", "view"]
        },
        "items": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["action", "items"]
}

SHOPPING_PROMPT = """
Extract shopping-list details from the user's message into a JSON object
with these fields:

- action: "add" | "remove" | "view"
  - "add" for adding items, or noting the user is low on / needs something
  - "remove" for taking items off the list
  - "view" for asking what's on the list — items should be an empty array
    for this action
- items: an array of clean item names, with filler words removed
  ("please", "to my list", "from the list", "we need", "some", "a bit of",
  etc.). Split multiple items into separate array entries, even if joined
  by "and", commas, or conversational filler between them. Keep each item
  name short and just the item itself (e.g. "milk", not "some milk please").

Never explain. Return only the JSON object.

Examples:

"Add milk to my shopping list"
{"action":"add","items":["milk"]}

"Add milk, eggs, and bread to my list"
{"action":"add","items":["milk","eggs","bread"]}

"We're out of milk and eggs, oh and also get some bread"
{"action":"add","items":["milk","eggs","bread"]}

"Remove rice from the list"
{"action":"remove","items":["rice"]}

"Take rice and onions off the list"
{"action":"remove","items":["rice","onions"]}

"What's on my shopping list?"
{"action":"view","items":[]}

"I'm running low on sugar, note that down"
{"action":"add","items":["sugar"]}
"""


def extract_shopping(user_text):
    payload = {
        "messages": [
            {"role": "system", "content": SHOPPING_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0,
        "max_tokens": 100,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "shopping_schema",
                "schema": SHOPPING_SCHEMA
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
            print("Shopping Extractor Server Error:", response.status_code)
            print("Shopping Extractor Error Body:", response.text)
            return None

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        print("\n========== SHOPPING EXTRACT RAW ==========")
        print(repr(content))
        print("============================================\n")

        return json.loads(content)

    except Exception as e:
        print("Shopping extraction error:", e)
        return None


# ----------------------------------------
# Close Session
# ----------------------------------------
def close_session():
    session.close()