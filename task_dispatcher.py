# ----------------------------------------
# Task Dispatcher
# ----------------------------------------
# Routes a classified intent to its handler.
# Every handler here is a FILLER — replace the body with real logic
# (JSON read/write, datetime lookups, etc.) as each feature is built.
# ----------------------------------------


def handle_conversation(user_text, result):
    print(f"[ROUTE] conversation -> passing to main LLM: \"{user_text}\"")
    return None  # signal to main.py: fall through to normal ask_llm()


def handle_emergency(user_text, result):
    print(f"[ROUTE] EMERGENCY triggered -> slots: {result.get('slots')}")
    # TODO: trigger caregiver notification (SMS/call/webhook)
    return "I'm alerting your emergency contact right now. Stay where you are."


def handle_time(user_text, result):
    action = result.get("action")
    print(f"[ROUTE] task -> time -> {action}")
    # TODO: replace with real datetime lookups based on `action`
    #   date_enquiry -> today's date
    #   day_enquiry  -> day of week
    #   time_enquiry -> current time
    return f"(filler) date enquiry handled — action={action}"


def handle_reminder(user_text, result):
    action = result.get("action")
    slots = result.get("slots")
    print(f"[ROUTE] task -> reminder -> {action} -> slots: {slots}")
    # TODO: parse slots into {content, time, recurrence} and write to reminders.json
    return f"(filler) set a reminder handled — slots={slots}"


def handle_shopping(user_text, result):
    action = result.get("action")
    slots = result.get("slots")
    print(f"[ROUTE] task -> shopping -> {action} -> slots: {slots}")
    # TODO: parse slots into {action: add/remove/list, item} and update shopping_list.json
    return f"(filler) shopping list handled — action={action}, slots={slots}"


def handle_event(user_text, result):
    action = result.get("action")
    slots = result.get("slots")
    print(f"[ROUTE] task -> event -> {action} -> slots: {slots}")
    # TODO: parse slots into {action: add/query, date_range, content} and update events.json
    return f"(filler) marked an event — action={action}, slots={slots}"


def handle_news(user_text, result):
    action = result.get("action")
    print(f"[ROUTE] task -> news -> {action}")
    # TODO: fetch/cache local headlines
    return "(filler) news headlines handled"


# ----------------------------------------
# Dispatch table
# ----------------------------------------
TASK_HANDLERS = {
    "time": handle_time,
    "reminder": handle_reminder,
    "shopping": handle_shopping,
    "event": handle_event,
    "news": handle_news,
}


def dispatch(user_text, result):
    intent = result.get("intent")

    if intent == "emergency":
        return handle_emergency(user_text, result)

    if intent == "conversation":
        return handle_conversation(user_text, result)

    if intent == "task":
        category = result.get("task_category")
        handler = TASK_HANDLERS.get(category)
        if handler:
            return handler(user_text, result)
        print(f"[ROUTE] Unknown task_category: {category}")
        return handle_conversation(user_text, result)

    # Unknown intent — safest fallback is normal conversation
    print(f"[ROUTE] Unknown intent: {intent}")
    return handle_conversation(user_text, result)