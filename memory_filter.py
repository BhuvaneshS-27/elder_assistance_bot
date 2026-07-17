QUESTION_WORDS = (
    "what",
    "when",
    "where",
    "who",
    "why",
    "how",
    "which",
    "can",
    "could",
    "should",
    "would",
    "is",
    "are",
    "do",
    "does",
    "did",
    "will",
    "may"
)

# --------------------------------------------------
# Uncertain statements
# --------------------------------------------------

UNCERTAIN_PHRASES = (
    "i think",
    "i guess",
    "i believe",
    "maybe",
    "perhaps",
    "probably",
    "possibly",
    "i'm not sure",
    "not sure",
    "i suspect",
    "i feel like",
    "i wonder if",
    "i hope",
    "i wish"
)

UNCERTAIN_WORDS = (
    "might",
    "may",
    "could",
)

# --------------------------------------------------
# Temporary states
# --------------------------------------------------

TEMPORARY_PHRASES = (

    "today",
    "right now",
    "currently",
    "at the moment",
    "this morning",
    "this afternoon",
    "this evening",
    "tonight",

    "i have a headache",
    "i have fever",
    "i have a fever",
    "i have cough",
    "i have a cough",

    "i'm tired",
    "i am tired",

    "i'm sleepy",
    "i am sleepy",

    "i'm hungry",
    "i am hungry",

    "i'm thirsty",
    "i am thirsty",

    "i'm sick",
    "i am sick",

    "i'm dizzy",
    "i am dizzy",

    "i'm feeling",
    "i am feeling"
)

# --------------------------------------------------
# One-time events
# --------------------------------------------------

EVENT_WORDS = (

    "yesterday",
    "tomorrow",
    "last night",
    "last week",
    "last month",
    "next week",
    "next month",

    "went",
    "visited",
    "bought",
    "sold",
    "met",
    "called",
    "travelled",
    "traveled",
    "arrived",
    "left",
    "ate",
    "drank",
    "watched",
    "played",
    "finished",
    "started"
)

# --------------------------------------------------
# Question
# --------------------------------------------------

def is_question(text: str) -> bool:

    t = text.lower().strip()

    if t.endswith("?"):
        return True

    return any(
        t.startswith(word + " ")
        for word in QUESTION_WORDS
    )

# --------------------------------------------------
# Uncertain
# --------------------------------------------------

def is_uncertain(text: str) -> bool:

    t = text.lower()

    if any(p in t for p in UNCERTAIN_PHRASES):
        return True

    words = t.split()

    return any(word in words for word in UNCERTAIN_WORDS)

# --------------------------------------------------
# Temporary
# --------------------------------------------------

def is_temporary(text: str) -> bool:

    t = text.lower()

    return any(
        phrase in t
        for phrase in TEMPORARY_PHRASES
    )

# --------------------------------------------------
# One-time event
# --------------------------------------------------

def is_one_time_event(text: str) -> bool:

    t = text.lower()

    words = t.split()

    if any(word in words for word in EVENT_WORDS):
        return True

    if any(word in t for word in EVENT_WORDS):
        return True

    return False

# --------------------------------------------------
# Main Decision
# --------------------------------------------------

def should_extract_memory(text: str) -> bool:

    if is_question(text):
        return False

    if is_uncertain(text):
        return False

    if is_temporary(text):
        return False

    if is_one_time_event(text):
        return False

    return True