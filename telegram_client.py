import requests
from secrets import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_emergency_alert(message):
    """
    Sends an emergency alert to the configured caregiver via Telegram.

    Returns True on success, False on failure (e.g. no internet, bad
    token/chat_id). The caller decides what to tell the user if this
    fails — we never silently pretend the alert went out.
    """
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }

    try:
        response = requests.post(TELEGRAM_API, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        print("Telegram alert error:", e)
        return False