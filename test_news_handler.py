from task_dispatcher import handle_news

fake_result = {"intent": "task", "task_category": "news", "action": "news_headlines", "slots": ""}

tests = [
    "What's in the news today?",
    "Tell me today's headlines.",
    "What's happening in technology?",
    "Any sports news?",
    "What's going on in business?",
]

for sentence in tests:
    print("=" * 70)
    print("INPUT :", sentence)
    reply = handle_news(sentence, fake_result)
    print("REPLY :", reply)