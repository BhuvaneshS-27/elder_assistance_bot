from task_dispatcher import handle_reminder
import reminder_store

tests = [
    "Remind me to take my tablets at 8 PM.",
    "Set a reminder to call my daughter tomorrow morning.",
    "I need to remember to water the plants every evening.",
    "Nudge me before my grandson's birthday next month.",
    "Make sure I don't miss my physiotherapy session every Monday.",
    "Ping me when it's time for my insulin shot.",
]

fake_result = {"intent": "task", "task_category": "reminder", "action": "set_reminder", "slots": ""}

for sentence in tests:
    print("=" * 70)
    print("INPUT :", sentence)
    reply = handle_reminder(sentence, fake_result)
    print("REPLY :", reply)

print("\n" + "=" * 70)
print("STORED REMINDERS:")
for r in reminder_store.list_reminders():
    print(r)