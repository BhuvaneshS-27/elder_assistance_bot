import json
import os
import uuid
from datetime import datetime, timedelta

REMINDERS_FILE = "reminders.json"

RECURRENCE_DELTAS = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
    "monthly": timedelta(days=30),   # approximate — good enough for v1
    "yearly": timedelta(days=365),
}


# ----------------------------------------
# Load / Save
# ----------------------------------------
def _load():
    if not os.path.exists(REMINDERS_FILE):
        return []
    try:
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)


# ----------------------------------------
# Add a new reminder
# ----------------------------------------
def add_reminder(content, due_time, recurrence="none"):
    reminders = _load()
    reminder = {
        "id": str(uuid.uuid4())[:8],
        "content": content,
        "due_time": due_time.isoformat(),
        "recurrence": recurrence,
        "notified": False,
        "created_at": datetime.now().isoformat(),
    }
    reminders.append(reminder)
    _save(reminders)
    return reminder


# ----------------------------------------
# Get reminders that are due and not yet notified
# ----------------------------------------
def get_due_reminders():
    reminders = _load()
    now = datetime.now()
    due = []
    for r in reminders:
        if r.get("notified"):
            continue
        try:
            due_time = datetime.fromisoformat(r["due_time"])
        except (KeyError, ValueError):
            continue
        if due_time <= now:
            due.append(r)
    return due


# ----------------------------------------
# Mark a reminder as delivered.
# Recurring reminders get rescheduled to their next occurrence
# instead of being marked permanently done.
# ----------------------------------------
def mark_notified(reminder_id):
    reminders = _load()
    for r in reminders:
        if r["id"] != reminder_id:
            continue

        recurrence = r.get("recurrence", "none")

        if recurrence in RECURRENCE_DELTAS:
            due_time = datetime.fromisoformat(r["due_time"])
            next_due = due_time + RECURRENCE_DELTAS[recurrence]
            r["due_time"] = next_due.isoformat()
            r["notified"] = False
        else:
            r["notified"] = True

    _save(reminders)


# ----------------------------------------
# List all reminders (for a future "what are my reminders" view)
# ----------------------------------------
def list_reminders():
    return _load()
