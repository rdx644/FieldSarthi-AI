"""Manual Windows microphone helper for WBS-01.1. Never runs during tests.
Microsoft MCI record/set: https://learn.microsoft.com/en-us/windows/win32/multimedia/record
https://learn.microsoft.com/en-us/windows/win32/multimedia/set
"""

import argparse
import ctypes
import os
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true", help="Consent to microphone recording")
    parser.add_argument("--seconds", type=int, choices=range(5, 26), default=12)
    args = parser.parse_args()
    if not args.record:
        parser.error("Use --record only when you are ready to speak and consent to recording")
    if os.name != "nt":
        parser.error("Windows only; use a recorder exporting mono PCM16 16kHz WAV")
    target = Path(__file__).resolve().parents[2] / "private/sample_hi.wav"
    target.parent.mkdir(exist_ok=True)
    if target.exists():
        parser.error("private/sample_hi.wav exists; rename it before recording another sample")
    winmm = ctypes.WinDLL("winmm")
    winmm.mciSendStringW.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint,
        ctypes.c_void_p,
    ]
    winmm.mciSendStringW.restype = ctypes.c_uint

    def command(text):
        code = winmm.mciSendStringW(text, None, 0, None)
        if code:
            raise RuntimeError(f"Windows recording command failed (MCI {code})")

    print("Say: Block B second floor ka water pump leak ho raha hai, urgent repair chahiye.")
    input(
        f"Press Enter to record your consenting voice for {args.seconds} seconds (Ctrl+C cancels): "
    )
    try:
        command("open new type waveaudio alias fieldsaarthi")
        command(
            "set fieldsaarthi format tag pcm channels 1 samplespersec 16000 "
            "bitspersample 16 alignment 2 bytespersec 32000"
        )
        command("record fieldsaarthi")
        print("Recording now...")
        time.sleep(args.seconds)
        command("stop fieldsaarthi")
        command(f'save fieldsaarthi "{target}"')
        print(f"Saved private recording: {target}")
        print("The live runner will validate its actual WAV format before uploading.")
    except RuntimeError as exc:
        print(f"{exc}. Check microphone permission or export the README WAV format manually.")
        return 1
    finally:
        winmm.mciSendStringW("close fieldsaarthi", None, 0, None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
