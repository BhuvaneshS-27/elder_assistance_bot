import requests
import json
from config import LLAMA_SERVER, INTENT_SCHEMA

# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------
session = requests.Session()

# ----------------------------------------
# System prompt for classification
# ----------------------------------------
ROUTER_PROMPT = """
You are an intent router for a voice assistant used by elderly people.

Classify the user's message into exactly one JSON object with these fields:

- intent: "conversation" | "task" | "emergency"
- task_category: "none" | "time" | "reminder" | "shopping" | "event" | "news" | "weather"
- action: a short snake_case label describing what the user wants
- slots: a short plain-text summary of any details mentioned (or empty string)

Rules:
1. "emergency" is for chest pain, falls, breathing trouble, "help me", or similar
   urgent situations. This overrides everything else.
2. "task" is for requests involving time/date, reminders, shopping lists,
   events/appointments, news headlines, or weather.
3. "conversation" is for everything else — greetings, small talk, opinions,
   general questions, emotional check-ins.
4. If intent is "conversation" or "emergency", task_category must be "none".
5. If the user is asking about their own availability or schedule
   (e.g. "am I free", "what's planned", "anything on my calendar"),
   classify as task_category "event", not "time". Reserve "time" for
   raw clock/date/day/year questions with no schedule-lookup intent.
6. Weather questions (rain, temperature, "hot/cold today", forecast, umbrella)
   are task_category "weather", never "news".
7. "current events", "what's new", "what's going on in the world" refer to
   news headlines, not calendar events — classify as task_category "news".
8. Never set intent to "task" with task_category "none". If the request
   doesn't map to time, reminder, shopping, event, news, or weather,
   classify it as "conversation" instead.
9. Never explain. Return only the JSON object.

Examples:

"Hi, how are you?"
{"intent":"conversation","task_category":"none","action":"greeting","slots":""}

"What day is it today?"
{"intent":"task","task_category":"time","action":"date_enquiry","slots":"today"}

"Is it still morning or afternoon?"
{"intent":"task","task_category":"time","action":"time_enquiry","slots":"morning or afternoon"}

"Am I free this Saturday?"
{"intent":"task","task_category":"event","action":"query_events","slots":"this Saturday"}

"Remind me to take my tablets at 8 PM"
{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"take tablets at 8 PM"}

"Add milk to my shopping list"
{"intent":"task","task_category":"shopping","action":"add_item","slots":"milk"}

"Take rice off my shopping list"
{"intent":"task","task_category":"shopping","action":"remove_item","slots":"rice"}

"Do you think it will rain later?"
{"intent":"task","task_category":"weather","action":"weather_forecast","slots":"rain later"}

"Should I carry an umbrella today?"
{"intent":"task","task_category":"weather","action":"weather_forecast","slots":"today"}

"Catch me up on current events"
{"intent":"task","task_category":"news","action":"news_headlines","slots":"current events"}

"I fell down and my leg hurts"
{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"fell down, leg pain"}
"""

# ----------------------------------------
# Classify user input
# ----------------------------------------
def classify_intent(user_text):
    payload = {
        "messages": [
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0,
        "max_tokens": 80,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "intent_schema",
                "schema": INTENT_SCHEMA
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
            print("Router LLM Server Error:", response.status_code)
            print("Router LLM Error Body:", response.text)
            return _fallback()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        print("\n========== ROUTER RAW ==========")
        print(repr(content))
        print("=================================\n")

        return json.loads(content)

    except Exception as e:
        print("Intent router error:", e)
        return _fallback()


def _fallback():
    # If classification fails for any reason, default to plain conversation
    # so the assistant still responds instead of silently failing.
    return {
        "intent": "conversation",
        "task_category": "none",
        "action": "fallback",
        "slots": ""
    }


# ----------------------------------------
# Close Session
# ----------------------------------------
def close_session():
    session.close()