# ----------------------------------------
# Task Dispatcher
# ----------------------------------------
# Routes a classified intent to its handler.
# Handlers marked FILLER are placeholders — replace the body with real
# logic (JSON read/write, API calls, etc.) as each feature is built.
# ----------------------------------------

from datetime import datetime, timedelta
import re

from llama_client import ask_time_fallback

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday"]


def handle_conversation(user_text, result):
    print(f"[ROUTE] conversation -> passing to main LLM: \"{user_text}\"")
    return None  # signal to main.py: fall through to normal ask_llm()


def handle_emergency(user_text, result):
    print(f"[ROUTE] EMERGENCY triggered -> slots: {result.get('slots')}")
    # TODO: trigger caregiver notification (SMS/call/webhook)
    return "I'm alerting your emergency contact right now. Stay where you are."


def handle_time(user_text, result):
    """
    Real implementation — no LLM call, pure datetime logic.

    The router's `action` field for time queries has proven inconsistent
    in testing (most questions come back as "date_enquiry" regardless of
    whether the user asked about the day, month, year, or clock time), so
    this handler determines what to answer from keywords in the raw
    user_text instead of trusting `action`.
    """
    text = user_text.lower()
    now = datetime.now()

    print(f"[ROUTE] task -> time -> action={result.get('action')} slots={result.get('slots')}")

    # "How many days left until Sunday?" / "days until Friday"
    for i, wd in enumerate(WEEKDAYS):
        if wd in text and ("until" in text or "left" in text or "days" in text):
            days_ahead = (i - now.weekday() + 7) % 7
            if days_ahead == 0:
                return f"Today is {wd.capitalize()}."
            plural = "day" if days_ahead == 1 else "days"
            return f"There are {days_ahead} {plural} left until {wd.capitalize()}."

    # "How long ago was yesterday?"
    if "yesterday" in text:
        yesterday = now - timedelta(days=1)
        return f"Yesterday was {yesterday.strftime('%A, %B %d')} — one day ago."

    # "How much time is left until 5" / "until 5:30" / "until 5 pm"
    # Checked before the generic time-of-day branch below, since sentences
    # like this contain the literal word "time" and would otherwise be
    # caught by that branch instead.
    match = re.search(r"until\s+(\d{1,2})(?!\d)(?::(\d{2}))?\s*(am|pm)?", text)
    if match and not any(wd in text for wd in WEEKDAYS):
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        meridiem = match.group(3)

        if meridiem:
            target_hour = (hour % 12) + (12 if meridiem == "pm" else 0)
            candidate_hours = [target_hour]
        else:
            # No am/pm given — consider both, pick whichever comes sooner
            candidate_hours = [hour % 12, (hour % 12) + 12]

        target_times = []
        for h in candidate_hours:
            target = now.replace(hour=h, minute=minute, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            target_times.append(target)

        target = min(target_times)
        total_minutes = int((target - now).total_seconds() // 60)
        hrs, mins = divmod(total_minutes, 60)

        parts = []
        if hrs > 0:
            parts.append(f"{hrs} hour{'s' if hrs != 1 else ''}")
        if mins > 0 or not parts:
            parts.append(f"{mins} minute{'s' if mins != 1 else ''}")

        return (
            f"There {'is' if total_minutes == 1 else 'are'} "
            f"{' and '.join(parts)} left until "
            f"{target.strftime('%I:%M %p').lstrip('0')}."
        )

    if "year" in text:
        return f"We're in the year {now.year}."

    if "month" in text:
        return f"This month is {now.strftime('%B')}."

    # Clock-time / time-of-day questions
    if any(kw in text for kw in ["time", "morning", "afternoon", "evening", "night"]):
        hour = now.hour
        if 5 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 17:
            period = "afternoon"
        elif 17 <= hour < 21:
            period = "evening"
        else:
            period = "night"
        return f"It's {now.strftime('%I:%M %p')} right now, so it's {period}."

    if "day" in text:
        return f"Today is {now.strftime('%A')}."

    if "date" in text:
        return f"Today's date is {now.strftime('%A, %B %d, %Y')}."

    # Fallback — no specific keyword matched. Rather than dumping a plain
    # date/time readout, let the LLM reason over the question using today's
    # date as context (handles things like "Has July started?", "Is
    # Christmas close?", "How many months are left this year?").
    print(f"[ROUTE] task -> time -> no keyword matched, using LLM fallback for: \"{user_text}\"")
    llm_reply = ask_time_fallback(user_text)

    if llm_reply:
        return llm_reply

    # If the LLM call itself failed (server down, timeout, etc.),
    # fall back to a plain readout so the user still gets an answer.
    print("[ROUTE] task -> time -> LLM fallback failed, using plain readout")
    return f"It's {now.strftime('%A, %B %d, %Y')}, {now.strftime('%I:%M %p')}."


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


def handle_weather(user_text, result):
    action = result.get("action")
    slots = result.get("slots")
    print(f"[ROUTE] task -> weather -> {action} -> slots: {slots}")
    # TODO: call a local/cached weather API (e.g. Open-Meteo) using a
    # configured location, and phrase the forecast in plain language
    # (e.g. "yes, carry an umbrella" rather than raw numbers).
    return f"(filler) weather forecast handled — slots={slots}"


# ----------------------------------------
# Dispatch table
# ----------------------------------------
TASK_HANDLERS = {
    "time": handle_time,
    "reminder": handle_reminder,
    "shopping": handle_shopping,
    "event": handle_event,
    "news": handle_news,
    "weather": handle_weather,
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