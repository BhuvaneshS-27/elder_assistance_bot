from collections import deque

from config import MAX_HISTORY


# --------------------------------------------------
# Conversation Memory
# --------------------------------------------------

conversation = deque(maxlen=MAX_HISTORY)


# --------------------------------------------------
# Add User Message
# --------------------------------------------------

def add_user_message(text):

    conversation.append(
        {
            "role": "user",
            "content": text
        }
    )


# --------------------------------------------------
# Add Assistant Message
# --------------------------------------------------

def add_assistant_message(text):

    conversation.append(
        {
            "role": "assistant",
            "content": text
        }
    )


# --------------------------------------------------
# Get Conversation History
# --------------------------------------------------

def get_history():

    return list(conversation)


# --------------------------------------------------
# Clear Conversation
# --------------------------------------------------

def clear_history():

    conversation.clear()


# --------------------------------------------------
# Print Conversation (Debug)
# --------------------------------------------------

def print_history():

    print("\n========== Conversation ==========")

    for msg in conversation:

        print(
            f"{msg['role'].capitalize()}: "
            f"{msg['content']}"
        )

    print("==================================\n")