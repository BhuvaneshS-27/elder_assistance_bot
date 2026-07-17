import requests
import time

from config import *

# ----------------------------------------
# Persistent HTTP Session
# ----------------------------------------

session = requests.Session()


# ----------------------------------------
# Transcribe Audio
# ----------------------------------------

def transcribe():

    try:

        with open(AUDIO_FILE, "rb") as f:

            files = {
                "file": f
            }

            data = {
                "temperature": "0.0",
                "response_format": "json"
            }

            # ----------------------------------------
            # Measure Whisper Request Time
            # ----------------------------------------

            request_start = time.perf_counter()

            response = session.post(
                WHISPER_SERVER,
                files=files,
                data=data,
                timeout=30
            )

            request_end = time.perf_counter()

        print(
            f"Whisper Request : "
            f"{request_end - request_start:.3f} sec"
        )

        if response.status_code != 200:

            print(
                "Server Error:",
                response.status_code
            )

            return ""

        # ----------------------------------------
        # Measure JSON Parsing Time
        # ----------------------------------------

        json_start = time.perf_counter()

        result = response.json()

        text = result["text"].strip()

        json_end = time.perf_counter()

        print(
            f"JSON Parse Time : "
            f"{(json_end - json_start) * 1000:.2f} ms"
        )

        return text

    except Exception as e:

        print(e)

        return ""


# ----------------------------------------
# Close Session
# ----------------------------------------

def close_session():

    session.close()