import json
import os

MEMORY_FILE = "long_term_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def update_memory(new_facts):

    if not new_facts:
        return

    memory = load_memory()

    changed = False

    for key, value in new_facts.items():

        if value is None:
            continue

        if memory.get(key) != value:

            memory[key] = value
            changed = True

    if changed:

        save_memory(memory)

        print("\n========== Long-Term Memory ==========")
        print(json.dumps(memory, indent=4))
        print("======================================\n")