import json
import requests
from datetime import datetime
from config import *
from memory import get_history
from long_term_memory import load_memory

# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------
session = requests.Session()


# ----------------------------------------
# Ask LLM (existing — unchanged)
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
# NEW: Lightweight time/date reasoning fallback
# ----------------------------------------
# Used only by task_dispatcher.handle_time() when no keyword branch
# matches the user's question. Deliberately skips SYSTEM_PROMPT, memory,
# and conversation history — it only needs today's date/time as context
# and the single user question, keeping it fast and focused rather than
# dragging in the full conversational prompt.
# ----------------------------------------
def ask_time_fallback(user_text):
    now = datetime.now()
    context = (
        f"Today's date is {now.strftime('%A, %B %d, %Y')}. "
        f"The current time is {now.strftime('%I:%M %p')}."
    )

    messages = [
        {
            "role": "system",
            "content": (
                f"{context} You are a voice assistant for an elderly person. "
                "Answer the user's date/time-related question in ONE short, "
                "natural sentence using the information above. If the "
                "question requires a calculation (e.g. days or months until "
                "something, or whether a date has passed), work it out "
                "yourself and give the answer directly. Do not explain your "
                "reasoning, do not add extra commentary."
            )
        },
        {"role": "user", "content": user_text}
    ]

    payload = {
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 60
    }

    try:
        response = session.post(
            LLAMA_SERVER + "/v1/chat/completions",
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            print("Time Fallback LLM Server Error:", response.status_code)
            return ""

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("Time fallback LLM error:", e)
        return ""


# ----------------------------------------
# Close Session
# ----------------------------------------
def close_session():
    session.close()