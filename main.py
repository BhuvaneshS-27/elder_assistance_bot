import time
import threading

from recorder import record_audio, calibrate_noise
from whisper_client import transcribe, close_session as close_whisper
from llama_client import ask_llm, close_session as close_llama
from tts_client import speak
from memory_filter import should_extract_memory
from fact_extractor import extract_facts
from long_term_memory import (
    update_memory,
    load_memory
)
from memory import (
    add_user_message,
    add_assistant_message,
    print_history
)
from intent_router import classify_intent, close_session as close_router
from task_dispatcher import dispatch
import reminder_store


# ---------------------------------
# Background fact extraction
# ---------------------------------
def run_fact_extraction_async(text):
    """
    Runs fact extraction + memory update on a background thread so it
    never blocks the main reply/TTS path. Fire-and-forget: whatever
    facts are found get written to long_term_memory whenever the
    thread finishes, even if that's after the assistant has already
    started speaking.
    """
    def worker():
        fact_start = time.perf_counter()

        if should_extract_memory(text):
            facts = extract_facts(text)
        else:
            print("\nSkipped memory extraction (question or uncertain statement).")
            facts = {}

        fact_end = time.perf_counter()
        print(f"[background] Fact Extraction : {fact_end - fact_start:.3f} sec")
        print("\n========== Extracted Facts ==========")
        print(facts)
        print("=====================================\n")

        if isinstance(facts, dict) and len(facts) > 0:
            update_memory(facts)

    threading.Thread(target=worker, daemon=True).start()


def main():
    print("=" * 50)
    print("Offline Voice Assistant Started")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    # ---------------------------------
    # Show saved long-term memory
    # ---------------------------------
    memory = load_memory()
    print("\n========== Long-Term Memory ==========")
    print(memory)
    print("======================================\n")

    # ---------------------------------
    # Microphone calibration
    # ---------------------------------
    calibrate_noise()

    while True:
        success, data = record_audio()

        # ---------------------------------
        # Due reminders fired during the
        # listening wait — announce them,
        # then go straight back to listening.
        # ---------------------------------
        if success == "reminder":
            for reminder in data:
                print(f"\n[REMINDER DUE] {reminder['content']}")
                speak(f"Reminder: {reminder['content']}")
                reminder_store.mark_notified(reminder["id"])
            continue

        if not success:
            continue

        speech_end_time = data

        # ---------------------------------
        # Speech → Text
        # ---------------------------------
        text = transcribe()
        text_output_time = time.perf_counter()
        print(
            f"Speech End → Text : "
            f"{text_output_time - speech_end_time:.3f} sec"
        )

        if text == "" or text == "[BLANK_AUDIO]":
            print("Ignored blank audio.")
            continue

        print("\nYou said:")
        print(text)

        # ---------------------------------
        # Short-Term Conversation Memory
        # ---------------------------------
        add_user_message(text)

        # ---------------------------------
        # Intent Classification (router)
        # ---------------------------------
        router_start = time.perf_counter()
        result = classify_intent(text)
        router_end = time.perf_counter()
        print(
            f"Intent Classification : "
            f"{router_end - router_start:.3f} sec"
        )
        print("\n========== Intent ==========")
        print(result)
        print("=============================\n")

        # ---------------------------------
        # Route: emergency / task / conversation
        # ---------------------------------
        llm_start = time.perf_counter()

        if result.get("intent") in ("emergency", "task"):
            reply = dispatch(text, result)
            if reply is None:
                # dispatcher fell through (e.g. unknown category) — use main LLM
                reply = ask_llm(text)
        else:
            reply = ask_llm(text)

        llm_end = time.perf_counter()
        print(
            f"Text → Reply : "
            f"{llm_end - llm_start:.3f} sec"
        )

        print("\nAssistant:")
        print(reply)

        # ---------------------------------
        # Store Assistant Reply
        # ---------------------------------
        add_assistant_message(reply)

        # ---------------------------------
        # Debug Conversation
        # ---------------------------------
        print_history()

        # ---------------------------------
        # Speak
        # ---------------------------------
        tts_start = time.perf_counter()
        speak(reply)
        tts_end = time.perf_counter()
        print(
            f"Reply → Speech : "
            f"{tts_end - tts_start:.3f} sec"
        )

        # ---------------------------------
        # Long-Term Memory Extraction
        # (fired AFTER speaking — only overlaps with audio playback,
        # not with the router/main LLM calls, avoiding contention
        # during the latency-critical Speech End → Voice Starts window)
        #
        # Only run this for genuine conversation turns. Task commands
        # ("remind me to...", "add milk to my list") are already
        # handled by their own dedicated storage (reminders.json,
        # shopping_list.json, etc.) — running fact extraction on them
        # too caused one-off commands to get saved as permanent
        # "facts" about the user (e.g. {"reminder": "take tablets in
        # 20 seconds"} showing up in long_term_memory.json forever).
        # ---------------------------------
        if result.get("intent") == "conversation":
            run_fact_extraction_async(text)

        print("-" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant stopped.")
    finally:
        close_whisper()
        close_llama()
        close_router()