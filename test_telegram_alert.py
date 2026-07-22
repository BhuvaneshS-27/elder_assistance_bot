from telegram_client import send_emergency_alert

result = send_emergency_alert(
    "This is a test alert from the Voice Assistant. "
    "If you received this, Telegram alerts are working correctly."
)

if result:
    print("Success — check the caregiver's Telegram for the test message.")
else:
    print("Failed — check TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, and your internet connection.")
    