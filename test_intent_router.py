from intent_router import classify_intent
from task_dispatcher import dispatch

tests = [
    # ---------- Conversation ----------
    "Hi, how are you?",
    "Come on.",
    "Tell me something interesting.",
    "I feel a bit lonely today.",

    # ---------- Time ----------
    "What day is it today?",
    "What's the time right now?",
    "What month is this?",

    # ---------- Reminder ----------
    "Remind me to take my tablets at 8 PM.",
    "Set a reminder to call my daughter tomorrow morning.",
    "Don't let me forget my doctor's appointment on Friday.",

    # ---------- Shopping ----------
    "Add milk to my shopping list.",
    "Remove rice from the list.",
    "What's on my shopping list?",

    # ---------- Event ----------
    "What appointments do I have next week?",
    "Mark that I have a dentist visit on Monday.",
    "Do I have anything planned this weekend?",

    # ---------- News ----------
    "What's in the news today?",
    "Tell me today's headlines.",

    # ---------- Emergency ----------
    "I fell down and my leg hurts.",
    "I'm having chest pain.",
    "Help me, I can't breathe properly.",

    # =====================================================
    # GENERALIZATION TESTS
    # None of these phrasings/keywords appear in ROUTER_PROMPT.
    # Goal: check if the model is actually reasoning about intent
    # rather than pattern-matching the exact example wording.
    # =====================================================

    # ---------- Conversation (novel phrasing) ----------
    "Good morning, did you sleep well?",
    "I'm bored, talk to me for a bit.",
    "Do you think it will rain later?",
    "What's your favourite season?",
    "I miss my late husband sometimes.",
    "You're a good listener.",
    "Sing me a little tune.",

    # ---------- Time (novel phrasing, no "date/time/month" keywords) ----------
    "How many days left until Sunday?",
    "Is it still morning or afternoon now?",
    "What year are we in?",
    "How long ago was yesterday?",

    # ---------- Reminder (novel phrasing, no "remind/reminder" keyword) ----------
    "Ping me when it's time for my insulin shot.",
    "I need to remember to water the plants every evening.",
    "Nudge me before my grandson's birthday next month.",
    "Make sure I don't miss my physiotherapy session.",

    # ---------- Shopping (novel phrasing, no "shopping list/add/remove" keyword) ----------
    "I'm running low on sugar, note that down.",
    "Take rice off whatever I need to buy.",
    "We need more coconut oil at home.",
    "What all do I still need to pick up from the store?",

    # ---------- Event (novel phrasing, no "appointment/event" keyword) ----------
    "Put it in my calendar that Ravi is visiting on Tuesday.",
    "Anything scheduled for tomorrow?",
    "I have a checkup coming up, note the date as the 14th.",
    "Am I free this Saturday?",

    # ---------- News (novel phrasing, no "news/headlines" keyword) ----------
    "What's happening in the world today?",
    "Anything important going on that I should know about?",
    "Catch me up on current events.",

    # ---------- Emergency (novel phrasing, no "help/fell/chest pain" keyword) ----------
    "Everything is spinning and I feel like I might pass out.",
    "There's blood coming from my arm, quite a lot.",
    "I think something is seriously wrong, I can't move my left side.",
    "The pain is unbearable, I don't know what to do.",

    # ---------- Ambiguous / tricky edge cases ----------
    "Remind me what day my son's flight lands.",       # reminder vs event vs time overlap
    "I bought vegetables today, add tomatoes to next week's list.",  # shopping, past+future mixed
    "It's been ages since I checked the news, what's new?",  # news, indirect
    "My chest has felt tight since this morning, should I worry?",  # emergency vs conversation
]

for sentence in tests:
    print("=" * 80)
    print("INPUT:")
    print(sentence)

    result = classify_intent(sentence)
    print("\nCLASSIFIED:")
    print(result)

    reply = dispatch(sentence, result)
    print("\nDISPATCH RESULT:")
    print(reply)