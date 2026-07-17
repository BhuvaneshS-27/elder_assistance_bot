import sounddevice as sd
import soundfile as sf
import numpy as np
import webrtcvad
import time

from collections import deque

from config import *

vad = webrtcvad.Vad(VAD_MODE)

# --------------------------------------------------
# Global Noise Estimate
# --------------------------------------------------

noise_level = None
initial_noise_level = None


# --------------------------------------------------
# Compute RMS Volume
# --------------------------------------------------

def compute_volume(audio):

    audio = audio.astype(np.float32)

    rms = np.sqrt(np.mean(audio ** 2))

    return rms / 32768.0


# --------------------------------------------------
# Initial Noise Calibration
# --------------------------------------------------

def calibrate_noise():

    global noise_level
    global initial_noise_level

    print("\nCalibrating microphone...")
    print("Please remain silent for 2 seconds.\n")

    frames = int(2 * SAMPLE_RATE / FRAME_SIZE)

    volumes = []

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=FRAME_SIZE,
    ) as stream:

        for _ in range(frames):

            audio, overflow = stream.read(FRAME_SIZE)

            volumes.append(compute_volume(audio))

    noise_level = np.mean(volumes)

    initial_noise_level = noise_level

    threshold = max(
        MIN_VOLUME,
        noise_level * NOISE_MULTIPLIER
    )

    print(f"Background Noise : {noise_level:.5f}")
    print(f"Initial Threshold: {threshold:.5f}")
    print("-" * 50)


# --------------------------------------------------
# Record Audio
# --------------------------------------------------

def record_audio():

    global noise_level
    global initial_noise_level

    pre_buffer = deque(
        maxlen=int(PRE_SPEECH * 1000 / FRAME_DURATION)
    )

    recorded_frames = []

    recording = False

    speech_window = deque(maxlen=WINDOW_SIZE)
    silence_window = deque(maxlen=WINDOW_SIZE)

    silent_frames = 0

    max_silent_frames = int(
        SILENCE_TIMEOUT * 1000 / FRAME_DURATION
    )

    speech_end_time = None

    print("\nWaiting for speech...")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=FRAME_SIZE,
    ) as stream:

        while True:

            audio, overflow = stream.read(FRAME_SIZE)

            audio_bytes = audio.tobytes()

            volume = compute_volume(audio)

            speech = vad.is_speech(
                audio_bytes,
                SAMPLE_RATE
            )

            threshold = max(
                MIN_VOLUME,
                noise_level * NOISE_MULTIPLIER
            )

            # ----------------------------------------
            # Learn background noise ONLY when idle
            # ----------------------------------------

            if (
                not recording
                and not speech
                and volume < threshold
            ):

                noise_level = (
                    NOISE_ALPHA * noise_level
                    + (1.0 - NOISE_ALPHA) * volume
                )

                # Prevent threshold drift
                noise_level = min(
                    noise_level,
                    initial_noise_level * MAX_NOISE_FACTOR
                )

                threshold = max(
                    MIN_VOLUME,
                    noise_level * NOISE_MULTIPLIER
                )

            speech_detected = (
                speech and
                volume > threshold
            )

            pre_buffer.append(audio.copy())

            speech_window.append(int(speech_detected))
            silence_window.append(int(speech_detected))

            speech_votes = sum(speech_window)

            confidence = speech_votes / max(
                1,
                len(speech_window)
            )

            # ----------------------------------------
            # Waiting for speech
            # ----------------------------------------

            if not recording:

                print(
                    f"\rNoise={noise_level:.4f} | "
                    f"Vol={volume:.4f} | "
                    f"Thr={threshold:.4f} | "
                    f"Conf={confidence*100:5.1f}%",
                    end=""
                )

                if len(speech_window) == WINDOW_SIZE:

                    if speech_votes >= START_THRESHOLD:

                        print("\nSpeech confirmed!")

                        recording = True

                        recorded_frames.extend(pre_buffer)

                        recorded_frames.append(audio.copy())

                        silence_window.clear()

                        silent_frames = 0

                continue

            # ----------------------------------------
            # Recording
            # ----------------------------------------

            recorded_frames.append(audio.copy())

            if len(silence_window) == WINDOW_SIZE:

                speech_votes = sum(silence_window)

                if speech_votes <= STOP_THRESHOLD:

                    silent_frames += 1

                else:

                    silent_frames = 0

                if silent_frames >= max_silent_frames:

                    speech_end_time = (
                        time.perf_counter()
                        - (silent_frames * FRAME_DURATION / 1000.0)
                    )

                    print("Silence detected.")

                    break

    # ----------------------------------------
    # Nothing recorded
    # ----------------------------------------

    if len(recorded_frames) == 0:

        return False, None

    audio = np.concatenate(recorded_frames)

    duration = len(audio) / SAMPLE_RATE

    if duration < MIN_RECORDING_DURATION:

        print(
            f"Ignored short recording ({duration:.2f} sec)"
        )

        return False, None

    # ----------------------------------------
    # Measure WAV saving time
    # ----------------------------------------

    wav_start = time.perf_counter()

    sf.write(
        AUDIO_FILE,
        audio,
        SAMPLE_RATE
    )

    wav_end = time.perf_counter()

    print(
        f"WAV Save Time : {(wav_end - wav_start) * 1000:.1f} ms"
    )

    print(f"Audio saved ({duration:.2f} sec)")

    return True, speech_end_time