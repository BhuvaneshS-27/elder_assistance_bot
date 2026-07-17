import time

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

        success, speech_end_time = record_audio()

        if not success:
            continue

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
        # Long-Term Memory Extraction
        # ---------------------------------

        fact_start = time.perf_counter()

        if should_extract_memory(text):

            facts = extract_facts(text)

        else:

            print(
                "\nSkipped memory extraction "
                "(question or uncertain statement)."
            )

            facts = {}

        fact_end = time.perf_counter()

        print(
            f"Fact Extraction : "
            f"{fact_end - fact_start:.3f} sec"
        )

        print("\n========== Extracted Facts ==========")
        print(facts)
        print("=====================================\n")

        if isinstance(facts, dict) and len(facts) > 0:

            update_memory(facts)

        # ---------------------------------
        # Short-Term Conversation Memory
        # ---------------------------------

        add_user_message(text)

        # ---------------------------------
        # Ask Main LLM
        # ---------------------------------

        llm_start = time.perf_counter()

        reply = ask_llm(text)

        llm_end = time.perf_counter()

        print(
            f"Text → LLM Reply : "
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
            f"LLM Reply → Speech : "
            f"{tts_end - tts_start:.3f} sec"
        )

        print("-" * 50)


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nAssistant stopped.")

    finally:

        close_whisper()
        close_llama()