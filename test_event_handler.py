from task_dispatcher import handle_event
import event_store

fake_result = {"intent": "task", "task_category": "event", "action": "", "slots": ""}

tests = [
    "Mark that I have a dentist visit on Monday.",
    "Put it in my calendar that Ravi is visiting on Tuesday at 3 PM.",
    "I have a checkup coming up, note the date as the 14th.",
    "What appointments do I have next week?",
    "Am I free this Saturday?",
    "Do I have anything planned this weekend?",
]

for sentence in tests:
    print("=" * 70)
    print("INPUT :", sentence)
    reply = handle_event(sentence, fake_result)
    print("REPLY :", reply)

print("\n" + "=" * 70)
print("STORED EVENTS:")
for e in event_store.list_all_events():
    print(e)