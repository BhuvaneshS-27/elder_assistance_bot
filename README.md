# Offline Voice Assistant for Elderly People

An offline AI voice assistant designed specifically for elderly people. The assistant performs speech recognition, classifies user intent, routes requests to task-specific handlers or a conversational LLM, remembers important user information across sessions, and generates natural voice responses — all while keeping every interaction completely local.

The project is optimized to run on a **Raspberry Pi 4 (4GB)** and uses lightweight, quantized local AI models to ensure privacy and low hardware requirements. Currently developed and benchmarked on PC; Pi4 deployment and re-benchmarking is in progress.

---

## Features

- Fully offline speech recognition using **Whisper.cpp**
- **LLM-based intent routing** — classifies each utterance as conversation, task, or emergency using structured JSON output (`response_format: json_schema`) from a single shared model
- **Task dispatch system** covering time, reminders, shopping lists, events/calendar, news, and weather — with a fallback to an LLM reasoning call for questions no rule-based handler covers
- Offline conversational AI using **Qwen2.5-1.5B (GGUF Quantized)** via **llama.cpp**
- Offline text-to-speech using **Piper**
- Voice Activity Detection using **WebRTC VAD**
- Short-term conversation memory
- Persistent long-term memory stored as JSON
- **Background, non-blocking fact extraction** — runs on a separate thread after the reply is spoken, so it never adds latency to the conversation
- Intelligent filtering to avoid storing temporary or uncertain information
- Personalized conversations using stored memory
- Basic emergency-phrase detection with a placeholder caregiver-alert hook
- No cloud services required after setup — every model runs locally

---

## Current Architecture

```
Microphone
     │
     ▼
WebRTC Voice Activity Detection
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
     │              ├── time      (real — pure Python/datetime, LLM fallback for edge cases)
     │              ├── reminder  (stub)
     │              ├── shopping  (stub)
     │              ├── event     (stub)
     │              ├── news      (stub)
     │              └── weather   (stub)
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
                      (fires after reply is spoken, not before)
```

The intent router and main conversational LLM share a **single loaded model** via one `llama-server` instance running with `--parallel` slots, rather than loading separate model copies — important for staying within the Raspberry Pi 4's 4GB RAM budget.

---

## Technologies

- Python
- Whisper.cpp
- llama.cpp (with `--parallel` multi-slot serving)
- Qwen2.5-1.5B (GGUF Quantized)
- Piper TTS
- WebRTC VAD
- JSON

---

## Example

**User**
> My name is Ravi.

**Assistant**
> Hello Ravi! How can I help you today?

The assistant automatically remembers the user's name and uses it naturally in future conversations.

**User**
> What day is it today?

**Assistant**
> Today is Sunday.

This is answered instantly by the `time` task handler — no LLM call needed for straightforward date/time questions.

---

## Current Status / Known Limitations

This project is under active development. Current state:

- **Task handlers**: only `time` is fully implemented (pure Python, keyword-routed, with an LLM fallback for questions outside its keyword coverage). `reminder`, `shopping`, `event`, `news`, and `weather` are wired into the router and dispatcher but still return placeholder responses.
- **Intent router accuracy**: ~98% on an internal 60-case test suite covering both direct and generalized/novel phrasing. Test suite lives alongside the code and is extended as new task categories are added.
- **Latency (PC, not yet Pi4)**: Speech End → Text ~2.2s, Intent Classification ~0.65–0.75s, main LLM reply ~0.4–0.6s, Piper synthesis ~0.4–0.5s. Whisper STT is currently the largest single stage and hasn't been optimized yet.
- **Not yet tested on actual Raspberry Pi 4 hardware** — all development and benchmarking so far is on PC. ARM performance is expected to differ meaningfully from PC numbers.
- **Streaming TTS** (speaking as the reply is generated, rather than waiting for the full response) has been identified as the next major latency improvement but isn't implemented yet.
- **Short-term conversation memory** has no length cap yet — long sessions may eventually hit model context-size limits.
- Emergency detection relies on the LLM router; a rule-based/keyword safety-net alongside it is planned but not yet built.

---

## Future Work

- Build out `reminder`, `shopping`, `event`, `news`, and `weather` task handlers (JSON-backed storage, following the same pattern as `time`)
- Local calculator tool (not yet started)
- Streaming TTS for faster perceived response time
- Whisper.cpp optimization (English-only model variant, timestamp/beam-size tuning)
- Raspberry Pi 4 deployment and real-hardware benchmarking
- Rule-based emergency keyword detection as a safety net alongside LLM classification
- Conversation memory capping/summarization for long sessions
- Structured per-category slot schemas (currently a loose string, to be tightened per task type)
- Caregiver notification integration (SMS/call/webhook) for emergency alerts

---

## Project Goal

Build a private, lightweight, fully offline AI companion capable of assisting elderly people with everyday conversations and daily tasks — time, reminders, shopping lists, calendar events, news, and weather — while running efficiently on a Raspberry Pi 4.