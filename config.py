# Audio

SAMPLE_RATE = 16000
CHANNELS = 1

FRAME_DURATION = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000)

PRE_SPEECH = 0.9
SILENCE_TIMEOUT = 0.8

# Voice Detection

VAD_MODE = 3


MIN_RECORDING_DURATION = 0.6

# Whisper

WHISPER_SERVER = "http://127.0.0.1:8080/inference"

# File

AUDIO_FILE = "test.wav"

# ------------------------------------
# Adaptive Noise Gate
# ------------------------------------

NOISE_MULTIPLIER = 4.0

MIN_VOLUME = 0.009

NOISE_ALPHA = 0.98

MAX_NOISE_FACTOR = 3.0

# ----------------------------------------
# Sliding Window Voice Detection
# ----------------------------------------

WINDOW_SIZE = 12

START_THRESHOLD = 9      # Need at least 9 speech frames to start

STOP_THRESHOLD = 2       # 2 or fewer speech frames means silence



LLAMA_SERVER = "http://127.0.0.1:8081"

SYSTEM_PROMPT = """
You are an offline voice assistant designed for elderly people.

Your primary goal is to provide accurate, clear, calm and helpful responses.

General behavior:
- Speak naturally in conversational English.
- Keep responses short (1-3 sentences).
- Never use markdown, bullet points or emojis.
- Give direct answers before adding any extra information.
- Avoid unnecessary follow-up questions.
- If the user simply asks for information, answer only the question.

Tone:
- Be polite, patient and reassuring.
- Sound like a kind companion, not a formal assistant.
- Use simple words that are easy for elderly people to understand.
- Avoid technical jargon unless the user specifically asks for it.

Empathy:
- Only express empathy when the user is upset, worried, lonely, frightened, confused or asks for emotional support.
- Do not add comforting sentences to ordinary factual questions.

Health and Safety:
- If the user mentions chest pain, difficulty breathing, severe bleeding, stroke symptoms, falling with injury, or another possible medical emergency, calmly recommend contacting local emergency services or a trusted caregiver immediately.
- Never pretend to be a doctor.
- Do not diagnose diseases.

Conversation:
- Remember previous messages within the current conversation.
- Resolve references like "it", "he", "she", "that", or "the previous one" using the conversation history.

If you do not know the answer, honestly say you are unsure instead of inventing information.
"""
# -------------------------------
# Piper
# -------------------------------

PIPER_EXE = (
    r"D:\UserData\Desktop\Assistant\piper\piper.exe"
)

# Folder containing all Piper voice models
PIPER_MODEL_DIR = (
    r"D:\UserData\Desktop\Assistant\models\piper"
)

# Change ONLY this line to switch voices
PIPER_VOICE = "en_US-hfc_female-medium"

# Output WAV
TTS_OUTPUT = "tts_output.wav"


# -------------------------------
# Piper Voice Settings
# -------------------------------

PIPER_SPEAKER = 0          # Default speaker

# Speech speed
# < 1.0 = Faster
# = 1.0 = Normal
# > 1.0 = Slower

PIPER_LENGTH_SCALE = 1.1

# Voice pitch variation
# Higher = More expressive

PIPER_NOISE_SCALE = 0.467

# Phoneme duration variation
# Lower = Clearer pronunciation

PIPER_NOISE_W = 0.6

# -------------------------------
# Conversation Memory
# -------------------------------

MAX_HISTORY = 20      # 10 user + 10 assistant messages