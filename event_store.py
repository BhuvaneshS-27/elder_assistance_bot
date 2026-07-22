import json
import os
import uuid
from datetime import date, datetime

EVENTS_FILE = "events.json"


def _load():
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)


# ----------------------------------------
# Add an event. time_of_day is (hour, minute) or None if not given —
# stored as null rather than a fabricated default, since a made-up
# time would get spoken back to the user as if it were true.
# ----------------------------------------
def add_event(content, event_date, time_of_day=None):
    events = _load()

    entry = {
        "id": str(uuid.uuid4())[:8],
        "content": content,
        "date": event_date.isoformat(),
        "time": f"{time_of_day[0]:02d}:{time_of_day[1]:02d}" if time_of_day else None,
        "created_at": datetime.now().isoformat(),
    }

    events.append(entry)
    _save(events)
    return entry


# ----------------------------------------
# Query events within an inclusive date range
# ----------------------------------------
def query_events(start_date, end_date):
    events = _load()
    matched = []

    for e in events:
        try:
            e_date = date.fromisoformat(e["date"])
        except (KeyError, ValueError):
            continue
        if start_date <= e_date <= end_date:
            matched.append(e)

    matched.sort(key=lambda e: (e["date"], e["time"] or ""))
    return matched


def list_all_events():
    return _load()
