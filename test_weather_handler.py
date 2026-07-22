from task_dispatcher import handle_weather

fake_result = {"intent": "task", "task_category": "weather", "action": "weather_forecast", "slots": ""}

tests = [
    "Do you think it will rain later?",       # rain-only -> narrow rain reply
    "Should I carry an umbrella today?",      # rain-only -> narrow rain reply
    "Is it hot outside right now?",           # temp-only -> narrow temp reply
    "Is it cold today?",                      # temp-only -> narrow temp reply
    "What's it like outside?",                # general -> full report
    "Is it hot and will it rain later?",      # both keywords -> full report
]

for sentence in tests:
    print("=" * 70)
    print("INPUT :", sentence)
    reply = handle_weather(sentence, fake_result)
    print("REPLY :", reply)