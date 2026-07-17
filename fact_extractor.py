import requests

from config import *
from memory import get_history
import json
import re
# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------

session = requests.Session()


# ----------------------------------------
# Ask LLM
# ----------------------------------------

def extract_facts(user_text):

    # ----------------------------------------
    # Build conversation
    # ----------------------------------------

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    # Append complete conversation history
    messages.extend(get_history())

    payload = {

    "messages": [

        {
            "role": "system",
            "content":
"""
You are a memory extraction engine.

Your job is to decide whether the user's latest sentence contains
long-term personal information that should be remembered.

Return ONLY one valid JSON object.

Do not explain.
Do not use markdown.
Do not write anything except JSON.

If there is nothing worth remembering return

{}

Rules

1. Extract ONLY facts explicitly stated.
2. Never guess.
3. Never invent information.
4. Never copy example values.
5. Create descriptive snake_case keys whenever needed.
6. Prefer meaningful keys instead of generic ones.
7. Store only information useful in future conversations.
8. Ignore temporary events.
9. Ignore questions.
10. Ignore general knowledge.
11. Ignore today's weather or current activities.
12.If the user's latest message is asking a question Never extract facts from questions.
13.Only extract facts from statements made by the user.
14.Never store information if the user is uncertain.

Examples

"My name is Ravi."

{"name":"Ravi"}

"My blood group is O+."

{"blood_group":"O+"}

"My grandson is Arjun."

{"grandson":"Arjun"}

"My wife is Lakshmi."

{"wife":"Lakshmi"}

"I have Parkinson's disease."

{"medical_condition":"Parkinson's disease"}

"I wear hearing aids."

{"uses_hearing_aid":true}

"I own a Labrador named Bruno."

{
    "pet_type":"Labrador",
    "pet_name":"Bruno"
}

"My favourite cricket team is CSK."

{
    "favorite_cricket_team":"CSK"
}

"My dentist is Dr Kumar."

{
    "dentist":"Dr Kumar"
}

"My cardiologist is Dr Rao."

{
    "cardiologist":"Dr Rao"
}

"My walking stick is kept near the sofa."

{
    "walking_stick_location":"near the sofa"
}

"I usually wake up at 5 AM."

{
    "wake_up_time":"5 AM"
}

"My emergency contact is Priya."

{
    "emergency_contact":"Priya"
}

"What is my daughter's name?"

{}

"When should I go to the hospital?"

{}

"Who is my doctor?"

{}

"Do I have diabetes?"

{}


"I think I have diabetes."

{}

"I might have diabetes."

{}

"I probably have arthritis."

{}

"I am having Diabetes."
{
    "medical_condition":"Diabetes"
}
"""
        },

        {
            "role": "user",
            "content": user_text
        }

    ],

    "temperature": 0,

    "max_tokens": 120
}

    try:

        response = session.post(

            LLAMA_SERVER + "/v1/chat/completions",

            json=payload,

            timeout=60

        )

        if response.status_code != 200:

            print(
                "LLM Server Error:",
                response.status_code
            )

            return ""

        result = response.json()

        content = result["choices"][0]["message"]["content"]
        print("\n========== RAW ==========")
        print(repr(content))
        print("=========================\n")
        # Find the first JSON object
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if not match:
            return {}

        content = match.group(0)
# Remove markdown code fences if present
        if content.startswith("```json"):
            content = content[7:]

        if content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()
        

        return json.loads(content)
    except Exception as e:

        print(e)

        return ""


# ----------------------------------------
# Close Session
# ----------------------------------------

def close_session():

    session.close()