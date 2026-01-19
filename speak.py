# speak.py
import sys
import pyttsx3

if len(sys.argv) < 2:
    sys.exit(0)

text = " ".join(sys.argv[1:])

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
except Exception as e:
    print("TTS error:", e)
