# Offline Voice Assistant for Elderly People

An offline AI voice assistant designed specifically for elderly people. The assistant performs speech recognition, maintains conversational context, remembers important user information across sessions, and generates natural voice responses—all while keeping every interaction completely local.

The project is optimized to run on a **Raspberry Pi 4** and uses lightweight local AI models to ensure privacy and low hardware requirements.

---

## Features

* Fully offline speech recognition using **Whisper.cpp**
* Offline conversational AI using **Qwen2.5-1.5B (GGUF Quantized)** via **llama.cpp**
* Offline text-to-speech using **Piper**
* Voice Activity Detection using **WebRTC VAD**
* Short-term conversation memory
* Persistent long-term memory stored as JSON
* Automatic fact extraction using a dedicated LLM
* Intelligent filtering to avoid storing temporary or uncertain information
* Personalized conversations using stored memory
* No cloud services required after setup

---

## Current Architecture

```text
Microphone
     │
     ▼
WebRTC Voice Activity Detection
     │
     ▼
Whisper.cpp
(Speech-to-Text)
     │
     ├──────────────► Memory Extraction LLM
     │                     │
     │                     ▼
     │              JSON Memory Storage
     │
     ▼
Conversation Memory
     │
     ▼
Qwen2.5-1.5B
(Main Assistant)
     │
     ▼
Piper TTS
     │
     ▼
Speaker
```

---

## Technologies

* Python
* Whisper.cpp
* llama.cpp
* Qwen2.5-1.5B (GGUF Quantized)
* Piper TTS
* WebRTC VAD
* JSON

---

## Example

**User**

> My name is Ravi.

**Assistant**

> Hello Ravi! How can I help you today?

The assistant automatically remembers the user's name and uses it naturally in future conversations.

---

## Future Work

* LLM-based intent classification
* Local tools (time, date, calculator)
* Medication reminders
* Shopping lists
* Calendar management
* Emergency assistance
* Raspberry Pi optimization
* Fully offline scheduling system

---

## Project Goal

Build a private, lightweight, fully offline AI companion capable of assisting elderly people with everyday conversations and daily activities while running efficiently on a Raspberry Pi 4.
