# tts_engine.py
import subprocess
import sys
import shlex

class TTSEngine:
    """
    TTS engine that spawns a separate Python process per utterance.
    Works reliably on Windows even while mic recording is active.
    """

    def speak(self, text):
        if not text:
            return

        # Quote text safely
        text_escaped = shlex.quote(text)

        # Launch speak.py as a separate process
        subprocess.Popen([sys.executable, "speak.py", text])
