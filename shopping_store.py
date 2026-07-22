import json
import os
import uuid
from datetime import datetime

SHOPPING_FILE = "shopping_list.json"


# ----------------------------------------
# Load / Save
# ----------------------------------------
def _load():
    if not os.path.exists(SHOPPING_FILE):
        return []
    try:
        with open(SHOPPING_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save(items):
    with open(SHOPPING_FILE, "w") as f:
        json.dump(items, f, indent=2)


def _normalize(name):
    return name.strip().lower()


# ----------------------------------------
# Add one or more items.
# Returns (added, duplicates) — duplicates are skipped, not re-added.
# ----------------------------------------
def add_items(item_names):
    items = _load()
    existing_normalized = {_normalize(i["name"]) for i in items}

    added = []
    duplicates = []

    for name in item_names:
        norm = _normalize(name)
        if not norm:
            continue
        if norm in existing_normalized:
            duplicates.append(name.strip())
            continue

        items.append({
            "id": str(uuid.uuid4())[:8],
            "name": name.strip(),
            "added_at": datetime.now().isoformat(),
        })
        existing_normalized.add(norm)
        added.append(name.strip())

    _save(items)
    return added, duplicates


# ----------------------------------------
# Remove one or more items (case-insensitive exact match).
# Returns (removed, not_found).
# ----------------------------------------
def remove_items(item_names):
    items = _load()

    removed = []
    not_found = []

    for name in item_names:
        norm = _normalize(name)
        match = next((i for i in items if _normalize(i["name"]) == norm), None)

        if match:
            items.remove(match)
            removed.append(match["name"])
        else:
            not_found.append(name.strip())

    _save(items)
    return removed, not_found


# ----------------------------------------
# List all current items
# ----------------------------------------
def list_items():
    return _load()