# Offline Voice Assistant for Elderly People

An offline AI voice assistant designed specifically for elderly people. The assistant performs speech recognition, classifies user intent, routes requests to task-specific handlers or a conversational LLM, remembers important user information across sessions, and generates natural voice responses — all while keeping every interaction completely local.

The project is optimized to run on a **Raspberry Pi 4 (4GB)** and uses lightweight, quantized local AI models to ensure privacy and low hardware requirements. Currently developed and benchmarked on PC; Pi4 deployment and re-benchmarking is next.

---

## Features

- Fully offline speech recognition using **Whisper.cpp**
- **LLM-based intent routing** — classifies each utterance as conversation, task, or emergency using structured JSON output (`response_format: json_schema`) from a single shared model
- **Task dispatch system** covering time, reminders, shopping lists, calendar events, weather, and India-focused news
- **Proactive reminders** — the assistant interrupts its own listening loop to speak a reminder the moment it's due, without needing the user to ask
- **Real emergency alerts** — detected emergency phrases send a live Telegram message to a configured caregiver, with honest failure messaging if the alert can't be sent
- Offline conversational AI using **Qwen2.5-1.5B (GGUF Quantized)** via **llama.cpp**
- Offline text-to-speech using **Piper**
- Voice Activity Detection using **WebRTC VAD**
- Short-term conversation memory
- Persistent long-term memory stored as JSON
- **Background, non-blocking fact extraction** — runs on a separate thread after the reply is spoken, and only for genuine conversational turns (not task commands), so it never adds latency or pollutes memory with one-off instructions
- Personalized conversations using stored memory
- Live weather via Open-Meteo (no API key required) and India-focused news via Google News RSS — both fail honestly with no internet rather than serving stale data as current
- No cloud services required for the core assistant; the one external integration (Telegram, for emergency alerts) is free and keyless beyond a one-time bot setup

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
     ├── emergency ──► Emergency Handler ──► Telegram alert to caregiver
     │
     ├── task ──► Task Dispatcher
     │              ├── time      (real — Python/datetime, LLM fallback for edge cases)
     │              ├── reminder  (real — LLM extracts structure, dateparser resolves time, JSON storage, recurrence + proactive alerts)
     │              ├── shopping  (real — LLM extracts multi-item add/remove/view, JSON storage)
     │              ├── event     (real — LLM extracts structure, Python resolves single dates & ranges, JSON storage)
     │              ├── weather   (real — Open-Meteo API, keyword-routed short/full replies)
     │              └── news      (real — Google News RSS, India edition, category-routed)
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

**All 6 task categories are now fully implemented**, alongside real emergency alerting — this is the first checkpoint where every originally-scoped feature has a working implementation behind it, rather than a placeholder.

---

## Technologies

- Python
- Whisper.cpp
- llama.cpp (with `--parallel` multi-slot serving)
- Qwen2.5-1.5B (GGUF Quantized)
- Piper TTS
- WebRTC VAD
- `dateparser` (natural-language time/date resolution for reminders and events)
- `feedparser` (RSS parsing for news)
- Open-Meteo (weather, no API key required)
- Google News RSS, India edition (news headlines)
- Telegram Bot API (emergency caregiver alerts)
- JSON (all local storage: memory, reminders, shopping list, events)

---

## Setup Notes

**Secrets are kept out of version control.** Telegram bot credentials live in a separate `secrets.py` (gitignored), not in `config.py`, so they can never accidentally end up committed to a public repo. To set this up:

1. Create a bot via `@BotFather` on Telegram (`/newbot`), and message it once yourself.
2. Get your `chat_id` by visiting `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and reading the `"chat":{"id": ...}` value.
3. Create `secrets.py` in the project root:
   ```python
   TELEGRAM_BOT_TOKEN = "your token here"
   TELEGRAM_CHAT_ID = "your chat id here"
   ```
4. Confirm `secrets.py` is listed in `.gitignore` before running anything.

`config.py` also needs `WEATHER_LATITUDE`/`WEATHER_LONGITUDE` set to the actual deployment location (not secret, safe to commit).

---

## Example

**User**
> Remind me to take my tablets at 8 PM.

**Assistant**
> Okay, I'll remind you to take tablets on Tuesday, July 21 at 08:00 PM.

*(the assistant proactively speaks the reminder on its own when it comes due, without being asked)*

**User**
> What's happening in business?

**Assistant**
> Here are the top headlines in business: First, HDFC Bank Hammered Worst Since 2008... Second, Yen weakens to 163 vs USD... Third, Maruti Suzuki Cars To Get Costlier By Up To Rs 30,000 From Aug 2026.

**User**
> I fell down and my leg hurts.

**Assistant**
> I'm alerting your emergency contact right now. Stay where you are.

*(a real Telegram message is sent to the configured caregiver, including what the user said)*

---

## Current Status / Known Limitations

This project is under active development. Current state:

- **All 6 task handlers are fully implemented and tested**: `time`, `reminder`, `shopping`, `event`, `weather`, `news`. Emergency alerting is also real (Telegram).
- **Intent router accuracy**: ~98% on an internal 60-case test suite covering both direct and generalized/novel phrasing, refined over several rounds against real observed failures.
- **Latency (PC, not yet Pi4)**: Speech End → Text ~2.2s, Intent Classification ~0.65–0.75s, main LLM reply ~0.4–0.6s, Piper synthesis ~0.4–0.5s. Whisper STT is currently the largest single stage and hasn't been optimized yet.
- **Not yet tested on actual Raspberry Pi 4 hardware** — all development and benchmarking so far is on PC. ARM performance is expected to differ meaningfully from PC numbers.
- **Streaming TTS** (speaking as the reply is generated, rather than waiting for the full response) has been identified as the next major latency improvement but isn't implemented yet.
- **Short-term conversation memory** has no length cap yet — long sessions may eventually hit model context-size limits.
- **Emergency alerts rely entirely on home WiFi** — there's no cellular/GSM fallback and no local physical alarm, by deliberate choice. If WiFi happens to be down at the moment of a real emergency, the assistant tells the user honestly rather than pretending the alert went out, but cannot reach the caregiver another way.
- News headlines are titles-only (no per-headline summary) — Google News' RSS description field is a jumbled aggregator link list rather than a clean summary, so it's intentionally omitted rather than read aloud garbled.
- A few small known date-handling ambiguities are left as deliberate judgment calls rather than bugs — e.g. saying "on Tuesday" when today is already Tuesday resolves to today, not next week.
- Test scripts for reminders/shopping/events write to the real JSON stores, so repeated test runs accumulate data rather than resetting.

---

## Future Work

- Raspberry Pi 4 deployment and real-hardware benchmarking
- Streaming TTS for faster perceived response time
- Whisper.cpp optimization (English-only model variant, timestamp/beam-size tuning)
- Local calculator tool (not yet started)
- Rule-based emergency keyword detection as a safety net alongside LLM classification
- Local physical alert (buzzer/LED) or GSM/SMS fallback for emergencies, for when WiFi is unavailable
- Conversation memory capping/summarization for long sessions
- Test data isolation so test scripts don't accumulate state in production JSON files
- Optional: per-headline summaries for news via a dedicated Indian publisher's feed, if titles-only proves too sparse in practice

---

## Project Goal

Build a private, lightweight, fully offline AI companion capable of assisting elderly people with everyday conversations and daily tasks — time, reminders, shopping lists, calendar events, news, and weather — while running efficiently on a Raspberry Pi 4.