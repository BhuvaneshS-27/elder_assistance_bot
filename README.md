# Offline Voice Assistant for Elderly People

An offline AI voice assistant designed specifically for elderly people. The assistant performs speech recognition, classifies user intent, routes requests to task-specific handlers or a conversational LLM, remembers important user information across sessions, and generates natural voice responses — all while keeping every interaction completely local.

The project is optimized to run on a **Raspberry Pi 4 (4GB)** and uses lightweight, quantized local AI models to ensure privacy and low hardware requirements. Currently developed and benchmarked on PC; Pi4 deployment and re-benchmarking is in progress.

---

## Features

- Fully offline speech recognition using **Whisper.cpp**
- **LLM-based intent routing** — classifies each utterance as conversation, task, or emergency using structured JSON output (`response_format: json_schema`) from a single shared model
- **Task dispatch system** covering time, reminders, shopping lists, calendar events, and weather, with news still to come
- **Proactive reminders** — the assistant interrupts its own listening loop to speak a reminder the moment it's due, without needing the user to ask
- Offline conversational AI using **Qwen2.5-1.5B (GGUF Quantized)** via **llama.cpp**
- Offline text-to-speech using **Piper**
- Voice Activity Detection using **WebRTC VAD**
- Short-term conversation memory
- Persistent long-term memory stored as JSON
- **Background, non-blocking fact extraction** — runs on a separate thread after the reply is spoken, and only for genuine conversational turns (not task commands), so it never adds latency or pollutes memory with one-off instructions
- Personalized conversations using stored memory
- Basic emergency-phrase detection with a placeholder caregiver-alert hook
- Live weather via Open-Meteo (no API key required) — fails honestly with no internet rather than serving stale data as current
- No cloud services or API keys required after setup

---

## Current Architecture

```
Microphone
     │
     ▼
WebRTC Voice Activity Detection ──► (periodically checks for due reminders while listening)
     │
     ▼
Whisper.cpp
(Speech-to-Text)
     │
     ▼
Intent Router (Qwen2.5-1.5B, structured JSON output)
     │
     ├── emergency ──► Emergency Handler (caregiver alert — placeholder)
     │
     ├── task ──► Task Dispatcher
     │              ├── time      (real — Python/datetime, LLM fallback for edge cases)
     │              ├── reminder  (real — LLM extracts structure, dateparser resolves time, JSON storage, recurrence + proactive alerts)
     │              ├── shopping  (real — LLM extracts multi-item add/remove/view, JSON storage)
     │              ├── event     (real — LLM extracts structure, Python resolves single dates & ranges, JSON storage)
     │              ├── weather   (real — Open-Meteo API, keyword-routed short/full replies)
     │              └── news      (stub)
     │
     └── conversation ──► Qwen2.5-1.5B (Main Assistant, with memory context)
                                │
                                ▼
                          Piper TTS
                                │
                                ▼
                            Speaker

(in parallel, off the critical path)
Transcribed Text ──► Background Thread ──► Fact Extraction LLM ──► JSON Memory Storage
                      (fires after reply is spoken, conversation turns only)
```

Every LLM-backed handler follows the same division of labor: a small structured extraction call gets the *what* (content, raw time phrase, action, items) while Python handles the *math* (date resolution, recurrence, storage) — this was adopted after finding the LLM unreliable at date/time arithmetic on its own.

The intent router and main conversational LLM share a **single loaded model** via one `llama-server` instance running with `--parallel` slots, rather than loading separate model copies — important for staying within the Raspberry Pi 4's 4GB RAM budget.

---

## Technologies

- Python
- Whisper.cpp
- llama.cpp (with `--parallel` multi-slot serving)
- Qwen2.5-1.5B (GGUF Quantized)
- Piper TTS
- WebRTC VAD
- `dateparser` (natural-language time/date resolution for reminders and events)
- Open-Meteo (weather, no API key required)
- JSON (all local storage: memory, reminders, shopping list, events)

---

## Example

**User**
> Remind me to take my tablets at 8 PM.

**Assistant**
> Okay, I'll remind you to take tablets on Tuesday, July 21 at 08:00 PM.

*(the assistant proactively speaks the reminder on its own when it comes due, without being asked)*

**User**
> Add milk, eggs, and bread to my list.

**Assistant**
> Added milk, eggs, and bread to your list.

**User**
> Is it cold today?

**Assistant**
> No, it's not cold — it's 33°C, so it's quite hot outside. Today's high is 35°C.

---

## Current Status / Known Limitations

This project is under active development. Current state:

- **Task handlers**: `time`, `reminder`, `shopping`, `event`, and `weather` are fully implemented and tested. `news` is still a placeholder stub — not yet started.
- **Intent router accuracy**: ~98% on an internal 60-case test suite covering both direct and generalized/novel phrasing, refined over several rounds against real observed failures.
- **Latency (PC, not yet Pi4)**: Speech End → Text ~2.2s, Intent Classification ~0.65–0.75s, main LLM reply ~0.4–0.6s, Piper synthesis ~0.4–0.5s. Whisper STT is currently the largest single stage and hasn't been optimized yet.
- **Not yet tested on actual Raspberry Pi 4 hardware** — all development and benchmarking so far is on PC. ARM performance is expected to differ meaningfully from PC numbers.
- **Streaming TTS** (speaking as the reply is generated, rather than waiting for the full response) has been identified as the next major latency improvement but isn't implemented yet.
- **Short-term conversation memory** has no length cap yet — long sessions may eventually hit model context-size limits.
- Emergency detection relies on the LLM router; a rule-based/keyword safety-net alongside it is planned but not yet built.
- A few small known date-handling ambiguities are left as deliberate judgment calls rather than bugs — e.g. saying "on Tuesday" when today is already Tuesday resolves to today, not next week.
- Test scripts for reminders/shopping/events write to the real JSON stores, so repeated test runs accumulate data rather than resetting.

---

## Future Work

- Build the `news` task handler (source, category support, caching, and offline-honesty all still to be designed)
- Local calculator tool (not yet started)
- Streaming TTS for faster perceived response time
- Whisper.cpp optimization (English-only model variant, timestamp/beam-size tuning)
- Raspberry Pi 4 deployment and real-hardware benchmarking
- Rule-based emergency keyword detection as a safety net alongside LLM classification
- Conversation memory capping/summarization for long sessions
- Caregiver notification integration (SMS/call/webhook) for emergency alerts
- Test data isolation so test scripts don't accumulate state in production JSON files

---

## Project Goal

Build a private, lightweight, fully offline AI companion capable of assisting elderly people with everyday conversations and daily tasks — time, reminders, shopping lists, calendar events, news, and weather — while running efficiently on a Raspberry Pi 4.