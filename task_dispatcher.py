# ----------------------------------------
# Task Dispatcher
# ----------------------------------------
# Routes a classified intent to its handler.
# Handlers marked FILLER are placeholders — replace the body with real
# logic (JSON read/write, API calls, etc.) as each feature is built.
# ----------------------------------------

from datetime import datetime, timedelta, date
import re
import dateparser

from llama_client import ask_time_fallback
from telegram_client import send_emergency_alert
from reminder_extractor import extract_reminder
import reminder_store
from shopping_extractor import extract_shopping
import shopping_store
from event_extractor import extract_event
import event_store
from weather_client import get_weather, describe_code
from news_client import get_headlines

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday"]


def handle_conversation(user_text, result):
    print(f"[ROUTE] conversation -> passing to main LLM: \"{user_text}\"")
    return None  # signal to main.py: fall through to normal ask_llm()


def handle_emergency(user_text, result):
    slots = result.get("slots", "")
    print(f"[ROUTE] EMERGENCY triggered -> slots: {slots}")

    message = (
        "EMERGENCY ALERT\n"
        "The assistant detected a possible emergency.\n"
        f"User said: \"{user_text}\"\n"
        f"Details: {slots}"
    )

    sent = send_emergency_alert(message)

    if sent:
        return "I'm alerting your emergency contact right now. Stay where you are."

    print("[ROUTE] EMERGENCY -> Telegram alert failed to send")
    return (
        "I tried to alert your emergency contact, but I couldn't reach them "
        "right now. Please try calling for help directly if you can."
    )


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


DEFAULT_REMINDER_HOUR = 9  # used when no explicit clock time is given at all

PERIOD_TIMES = {
    "morning": (9, 0),
    "afternoon": (15, 0),
    "evening": (19, 0),
    "night": (21, 0),
    "noon": (12, 0),
    "midnight": (0, 0),
}


def resolve_time_phrase(time_phrase):
    """
    Resolves a raw natural-language time phrase into a real datetime.

    dateparser handles absolute/relative expressions well ("8 PM",
    "next Monday", "in 20 seconds"), but doesn't reliably resolve bare
    period-of-day words ("evening", "tomorrow morning") on their own —
    those get stripped out and mapped to a sensible default hour instead.

    Also: if no explicit clock time is present anywhere in the phrase
    (e.g. just "Monday" or "next month"), dateparser tends to default
    to midnight or inherit whatever the current clock time happens to
    be — neither of which is a sensible reminder time. In that case we
    override to DEFAULT_REMINDER_HOUR instead.
    """
    now = datetime.now()
    text = time_phrase.lower()

    has_explicit_clock_time = bool(re.search(r"\d", text)) or "am" in text or "pm" in text

    period_hour = None
    remaining_text = text
    for period, hm in PERIOD_TIMES.items():
        if period in text:
            period_hour = hm
            remaining_text = text.replace(period, "").strip()
            break

    if period_hour is not None:
        if remaining_text:
            base = dateparser.parse(
                remaining_text,
                settings={"PREFER_DATES_FROM": "future", "RELATIVE_BASE": now}
            )
        else:
            base = now

        if base is None:
            return None

        candidate = base.replace(
            hour=period_hour[0], minute=period_hour[1], second=0, microsecond=0
        )

        if candidate <= now and not remaining_text:
            candidate += timedelta(days=1)

        return candidate

    parsed = dateparser.parse(
        time_phrase,
        settings={"PREFER_DATES_FROM": "future", "RELATIVE_BASE": now}
    )

    if parsed is None:
        return None

    if not has_explicit_clock_time:
        parsed = parsed.replace(
            hour=DEFAULT_REMINDER_HOUR, minute=0, second=0, microsecond=0
        )
        if parsed <= now:
            parsed += timedelta(days=1)

    return parsed


def handle_reminder(user_text, result):
    print(f"[ROUTE] task -> reminder -> extracting details from: \"{user_text}\"")

    extracted = extract_reminder(user_text)

    if not extracted:
        return "Sorry, I couldn't understand that reminder. Could you say it again?"

    content = (extracted.get("content") or "").strip()
    time_phrase = (extracted.get("time_phrase") or "").strip()
    recurrence = extracted.get("recurrence", "none")

    if not content or not time_phrase:
        return "Sorry, I couldn't understand that reminder. Could you say it again?"

    due_time = resolve_time_phrase(time_phrase)

    if due_time is None:
        print(f"[ROUTE] task -> reminder -> could not resolve '{time_phrase}'")
        return (
            f"I got that you want a reminder for '{content}', but I couldn't "
            f"work out the time '{time_phrase}'. Could you say the time differently?"
        )

    reminder_store.add_reminder(content, due_time, recurrence)

    time_str = due_time.strftime("%A, %B %d at %I:%M %p")
    print(f"[ROUTE] task -> reminder -> saved: content='{content}' due={time_str} recurrence={recurrence}")

    if recurrence != "none":
        return f"Okay, I'll remind you to {content} {recurrence}, starting {time_str}."
    return f"Okay, I'll remind you to {content} on {time_str}."


def _join_natural(names):
    """'milk' / 'milk and eggs' / 'milk, eggs, and bread'"""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{', '.join(names[:-1])}, and {names[-1]}"


def handle_shopping(user_text, result):
    print(f"[ROUTE] task -> shopping -> extracting details from: \"{user_text}\"")

    extracted = extract_shopping(user_text)

    if not extracted:
        return "Sorry, I couldn't understand that. Could you say the item again?"

    action = extracted.get("action")
    items = [i.strip() for i in (extracted.get("items") or []) if i and i.strip()]

    print(f"[ROUTE] task -> shopping -> action={action} items={items}")

    if action == "add":
        if not items:
            return "Sorry, I didn't catch what to add. Could you say the item again?"

        added, duplicates = shopping_store.add_items(items)
        parts = []
        if added:
            parts.append(f"Added {_join_natural(added)} to your list.")
        if duplicates:
            verb = "was" if len(duplicates) == 1 else "were"
            parts.append(f"{_join_natural(duplicates)} {verb} already on your list.")
        return " ".join(parts) if parts else "There was nothing new to add."

    if action == "remove":
        if not items:
            return "Sorry, I didn't catch what to remove. Could you say the item again?"

        removed, not_found = shopping_store.remove_items(items)
        parts = []
        if removed:
            parts.append(f"Removed {_join_natural(removed)} from your list.")
        if not_found:
            parts.append(f"I couldn't find {_join_natural(not_found)} on your list.")
        return " ".join(parts) if parts else "I couldn't find those items on your list."

    if action == "view":
        current = shopping_store.list_items()
        if not current:
            return "Your shopping list is empty."
        names = [item["name"] for item in current]
        return f"Your shopping list has {_join_natural(names)}."

    return "Sorry, I didn't understand that shopping request."


MONTH_NAMES = ["january", "february", "march", "april", "may", "june", "july",
               "august", "september", "october", "november", "december"]


def _add_one_month(d):
    """Adds one month to a date, capping the day if the target month is shorter."""
    import calendar
    if d.month == 12:
        return d.replace(year=d.year + 1, month=1)
    next_month = d.month + 1
    last_day = calendar.monthrange(d.year, next_month)[1]
    return d.replace(month=next_month, day=min(d.day, last_day))


def resolve_date_range(phrase):
    """
    Resolves a raw date/range phrase into an inclusive (start, end) date
    pair. Ranges ("next week", "this weekend") need genuinely different
    handling from single dates ("Monday", "the 14th") — dateparser alone
    only gives a single date, so range phrases are resolved by hand here
    before falling back to dateparser for everything else.
    """
    text = phrase.lower()
    today = datetime.now().date()

    if "weekend" in text:
        days_until_sat = (5 - today.weekday()) % 7
        sat = today + timedelta(days=days_until_sat)
        sun = sat + timedelta(days=1)
        return sat, sun

    if "next week" in text:
        days_until_next_monday = (7 - today.weekday()) % 7
        if days_until_next_monday == 0:
            days_until_next_monday = 7
        start = today + timedelta(days=days_until_next_monday)
        end = start + timedelta(days=6)
        return start, end

    if "this week" in text:
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end

    if "today" in text:
        return today, today

    if "tomorrow" in text:
        d = today + timedelta(days=1)
        return d, d

    for i, wd in enumerate(WEEKDAYS):
        if wd in text:
            days_ahead = (i - today.weekday() + 7) % 7
            if days_ahead == 0 and "next" in text:
                days_ahead = 7
            d = today + timedelta(days=days_ahead)
            return d, d

    parsed = dateparser.parse(
        phrase,
        settings={"PREFER_DATES_FROM": "future", "RELATIVE_BASE": datetime.now()}
    )
    if parsed:
        d = parsed.date()

        # dateparser doesn't reliably push bare day-of-month phrases
        # ("the 14th") past the current month boundary even with
        # PREFER_DATES_FROM="future" — if it landed in the past and no
        # month name was given, roll it forward by one month by hand.
        if d < today and not any(m in text for m in MONTH_NAMES):
            d = _add_one_month(d)

        return d, d

    return None, None


def resolve_clock_time_only(phrase):
    """Resolves a raw clock-time phrase (e.g. '3 PM') to (hour, minute), or None."""
    if not phrase:
        return None

    text = phrase.lower()

    for period, hm in PERIOD_TIMES.items():
        if period in text:
            return hm

    parsed = dateparser.parse(phrase, settings={"RELATIVE_BASE": datetime.now()})
    if parsed:
        return (parsed.hour, parsed.minute)

    return None


def handle_event(user_text, result):
    print(f"[ROUTE] task -> event -> extracting details from: \"{user_text}\"")

    extracted = extract_event(user_text)

    if not extracted:
        return "Sorry, I couldn't understand that. Could you say it again?"

    action = extracted.get("action")
    content = (extracted.get("content") or "").strip()
    date_phrase = (extracted.get("date_phrase") or "").strip()
    time_phrase = (extracted.get("time_phrase") or "").strip()

    print(f"[ROUTE] task -> event -> action={action} content='{content}' date_phrase='{date_phrase}' time_phrase='{time_phrase}'")

    if action == "add":
        if not content or not date_phrase:
            return "Sorry, I didn't catch the event details. Could you say that again?"

        start, end = resolve_date_range(date_phrase)

        if start is None:
            return (
                f"I got that you want to note '{content}', but I couldn't "
                f"work out the date '{date_phrase}'. Could you say the date differently?"
            )

        time_of_day = resolve_clock_time_only(time_phrase) if time_phrase else None
        event_store.add_event(content, start, time_of_day)

        date_str = start.strftime("%A, %B %d")
        if time_of_day:
            time_str = datetime(2000, 1, 1, *time_of_day).strftime("%I:%M %p")
            return f"Okay, I've noted {content} on {date_str} at {time_str}."
        return f"Okay, I've noted {content} on {date_str}."

    if action == "query":
        if date_phrase:
            start, end = resolve_date_range(date_phrase)
            if start is None:
                return f"I couldn't work out the date '{date_phrase}'. Could you rephrase?"
        else:
            start, end = datetime.now().date(), datetime.now().date() + timedelta(days=365)

        matches = event_store.query_events(start, end)

        if not matches:
            if start == end:
                return f"You have nothing planned on {start.strftime('%A, %B %d')}."
            return f"You have nothing planned between {start.strftime('%B %d')} and {end.strftime('%B %d')}."

        descriptions = []
        for e in matches:
            e_date = date.fromisoformat(e["date"])
            if e["time"]:
                hh, mm = map(int, e["time"].split(":"))
                time_str = datetime(2000, 1, 1, hh, mm).strftime("%I:%M %p")
                descriptions.append(f"{e['content']} on {e_date.strftime('%A, %B %d')} at {time_str}")
            else:
                descriptions.append(f"{e['content']} on {e_date.strftime('%A, %B %d')}")

        return "You have " + _join_natural(descriptions) + "."

    return "Sorry, I didn't understand that event request."


NEWS_CATEGORY_KEYWORDS = {
    "technology": ["tech", "technology"],
    "business": ["business", "economy", "market", "finance"],
    "health": ["health", "medical", "medicine"],
    "science": ["science", "environment"],
    "entertainment": ["entertainment", "movie", "movies", "celebrity", "arts"],
    "sports": ["sport", "sports"],
    "politics": ["politics", "political", "election"],
    "world": ["world", "international", "global"],
}


def _detect_news_category(text):
    text = text.lower()
    for category, keywords in NEWS_CATEGORY_KEYWORDS.items():
        if any(k in text for k in keywords):
            return category
    return "general"


def handle_news(user_text, result):
    category = _detect_news_category(user_text)
    print(f"[ROUTE] task -> news -> category={category}")

    headlines = get_headlines(category=category, count=3)

    if headlines is None:
        return "I don't have internet access right now, so I can't get the news."

    if not headlines:
        return "I couldn't find any headlines right now. Please try again in a bit."

    ordinals = ["First", "Second", "Third", "Fourth", "Fifth"]
    parts = []

    for i, item in enumerate(headlines):
        ordinal = ordinals[i] if i < len(ordinals) else "Next"
        line = f"{ordinal}, {item['title']}."
        if item["summary"]:
            summary = item["summary"].strip()
            if summary and summary[-1] not in ".!?":
                summary += "."
            line += f" {summary}"
        parts.append(line)

    category_label = f" in {category}" if category != "general" else ""
    intro = f"Here are the top headlines{category_label}:"

    return intro + " " + " ".join(parts)


HOT_KEYWORDS = ["hot", "warm"]
COLD_KEYWORDS = ["cold", "cool", "chilly"]
TEMP_KEYWORDS = HOT_KEYWORDS + COLD_KEYWORDS + ["temperature", "degrees"]
RAIN_KEYWORDS = ["rain", "umbrella", "wet", "shower", "drizzle", "storm"]


def _describe_temp_feel(temp):
    if temp >= 32:
        return "quite hot"
    if temp >= 24:
        return "warm"
    if temp >= 15:
        return "mild"
    return "cool"


def handle_weather(user_text, result):
    print("[ROUTE] task -> weather -> fetching current conditions")

    text = user_text.lower()
    weather = get_weather()

    if weather is None:
        return "I don't have internet access right now, so I can't check the weather."

    temp = weather.get("current_temp")

    if temp is None:
        return "I couldn't get the weather details right now. Please try again in a bit."

    description = describe_code(weather.get("current_code"))
    high = weather.get("today_high")
    low = weather.get("today_low")
    rain_chance = weather.get("rain_chance")

    is_temp_question = any(k in text for k in TEMP_KEYWORDS)
    is_rain_question = any(k in text for k in RAIN_KEYWORDS)

    # Narrow temperature question ("Is it hot outside?") — short,
    # focused reply instead of the full report.
    if is_temp_question and not is_rain_question:
        feel = _describe_temp_feel(temp)
        asked_hot = any(k in text for k in HOT_KEYWORDS)
        asked_cold = any(k in text for k in COLD_KEYWORDS)

        if asked_hot:
            is_actually_hot = feel in ("quite hot", "warm")
            prefix = "Yes, it's" if is_actually_hot else "No, it's not hot —"
        elif asked_cold:
            is_actually_cold = feel == "cool"
            prefix = "Yes, it's" if is_actually_cold else "No, it's not cold —"
        else:
            prefix = "It's currently"

        reply = f"{prefix} {temp:.0f}\u00b0C, so it's {feel} outside."
        if high is not None:
            reply += f" Today's high is {high:.0f}\u00b0C."
        return reply

    # Narrow rain question ("Should I carry an umbrella?") — short,
    # focused reply instead of the full report.
    if is_rain_question and not is_temp_question:
        parts = [f"It's currently {temp:.0f}\u00b0C and {description}."]
        if rain_chance is not None:
            parts.append(f"There's a {rain_chance:.0f}% chance of rain.")
            if rain_chance >= 40:
                parts.append("You might want to carry an umbrella.")
            else:
                parts.append("You probably won't need an umbrella.")
        return " ".join(parts)

    # General/ambiguous question ("What's it like outside?"), or a
    # question touching both temp and rain — give the full report.
    parts = [f"It's currently {temp:.0f}\u00b0C and {description}."]

    if high is not None and low is not None:
        parts.append(f"Today's high is {high:.0f}\u00b0C with a low of {low:.0f}\u00b0C.")

    if rain_chance is not None:
        parts.append(f"There's a {rain_chance:.0f}% chance of rain.")
        if rain_chance >= 40:
            parts.append("You might want to carry an umbrella.")

    return " ".join(parts)


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