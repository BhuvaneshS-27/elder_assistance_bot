import json
import requests

from config import *
from memory import get_history
from long_term_memory import load_memory

# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------

session = requests.Session()


# ----------------------------------------
# Ask LLM
# ----------------------------------------

def ask_llm(user_text):

    # ----------------------------------------
    # Load Long-Term Memory
    # ----------------------------------------

    long_term_memory = load_memory()

    # ----------------------------------------
    # Build Messages
    # ----------------------------------------

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    # ----------------------------------------
    # Inject Long-Term Memory
    # ----------------------------------------

    if len(long_term_memory) > 0:

        memory_text = (
    "The following JSON contains long-term facts "
    "about the user.\n"
    "Use these facts whenever they are relevant.\n"
    "Do not mention them unless needed.\n\n"
    + json.dumps(long_term_memory, indent=2)
)

        messages.append(
            {
                "role": "system",
                "content": memory_text
            }
        )

    # ----------------------------------------
    # Append Conversation History
    # ----------------------------------------

    messages.extend(get_history())

    # ----------------------------------------
    # Payload
    # ----------------------------------------

    payload = {

        "messages": messages,

        "temperature": 0.4,

        "max_tokens": 128

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

        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:

        print(e)

        return ""


# ----------------------------------------
# Close Session
# ----------------------------------------

def close_session():

    session.close()