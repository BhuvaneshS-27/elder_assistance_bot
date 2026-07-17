import subprocess
import time
import os
import simpleaudio as sa

from config import *


# --------------------------------------------------
# Construct model path automatically
# --------------------------------------------------

PIPER_MODEL = os.path.join(
    PIPER_MODEL_DIR,
    PIPER_VOICE + ".onnx"
)


# --------------------------------------------------
# Text -> Speech
# --------------------------------------------------

def speak(text):

    try:

        # ----------------------------------------
        # Generate Speech
        # ----------------------------------------

        tts_start = time.perf_counter()

        subprocess.run(
            [
                PIPER_EXE,

                "--model",
                PIPER_MODEL,

                "--output_file",
                TTS_OUTPUT,

                "--speaker",
                str(PIPER_SPEAKER),

                "--length_scale",
                str(PIPER_LENGTH_SCALE),

                "--noise_scale",
                str(PIPER_NOISE_SCALE),

                "--noise_w",
                str(PIPER_NOISE_W),
            ],

            input=text.encode("utf-8"),

            check=True,

            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        tts_end = time.perf_counter()

        print(
            f"Piper Synthesis : "
            f"{tts_end - tts_start:.3f} sec"
        )

        # ----------------------------------------
        # Play Speech
        # ----------------------------------------

        play_start = time.perf_counter()

        wave = sa.WaveObject.from_wave_file(
            TTS_OUTPUT
        )

        play = wave.play()

        play.wait_done()

        play_end = time.perf_counter()

        print(
            f"Playback Time : "
            f"{play_end - play_start:.3f} sec"
        )

    except Exception as e:

        print("TTS Error:", e)