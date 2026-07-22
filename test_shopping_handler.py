from task_dispatcher import handle_shopping
import shopping_store

fake_result = {"intent": "task", "task_category": "shopping", "action": "", "slots": ""}

tests = [
    "Add milk to my shopping list.",
    "Add milk, eggs, and bread to my list.",       # multi-item + duplicate (milk)
    "We're out of sugar and coconut oil.",         # multi-item, indirect phrasing
    "Remove rice from the list.",                  # not found yet (never added)
    "Remove milk and eggs from the list.",         # multi-item remove
    "Take onions off the list.",                   # not found
    "What's on my shopping list?",
]

for sentence in tests:
    print("=" * 70)
    print("INPUT :", sentence)
    reply = handle_shopping(sentence, fake_result)
    print("REPLY :", reply)

print("\n" + "=" * 70)
print("STORED SHOPPING LIST:")
for item in shopping_store.list_items():
    print(item)