import queue
import json
import threading
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class VoiceInput:
    """
    Handles Push-To-Talk voice input using Vosk and sounddevice.

    Usage:
        voice = VoiceInput("models/vosk-model-small-en-us-0.15")
        voice.on_result = callback_function  # called with recognized text
        voice.start()  # when PTT pressed
        voice.stop()   # when PTT released
    """

    def __init__(self, model_path, sample_rate=16000):
        self.sample_rate = sample_rate
        self.model = Model(model_path)
        self.queue = queue.Queue()
        self.recording = False
        self.on_result = None  # callback function

        # Audio stream setup
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=self._callback
        )
        self.stream.start()

    # ---------------------------
    # sounddevice callback
    # ---------------------------
    def _callback(self, indata, frames, time_info, status):
        if self.recording:
            self.queue.put(indata.copy())

    # ---------------------------
    # Start recording (PTT pressed)
    # ---------------------------
    def start(self):
        self.recording = True
        # Clear any previous frames
        while not self.queue.empty():
            self.queue.get()

    # ---------------------------
    # Stop recording (PTT released)
    # ---------------------------
    def stop(self):
        self.recording = False
        # Process recorded audio in a separate thread
        threading.Thread(target=self._process_audio, daemon=True).start()

    # ---------------------------
    # Process audio frames
    # ---------------------------
    def _process_audio(self):
        frames = []
        while not self.queue.empty():
            frames.append(self.queue.get())

        if not frames:
            return  # nothing recorded

        # Combine all frames into a single byte string
        audio_bytes = b"".join(f.tobytes() for f in frames)

        # Run Vosk recognition
        recognizer = KaldiRecognizer(self.model, self.sample_rate)
        recognizer.AcceptWaveform(audio_bytes)
        result_json = json.loads(recognizer.Result())
        text = result_json.get("text", "").strip()

        if text and self.on_result:
            # GUI-safe: call the callback
            try:
                self.on_result(text)
            except Exception as e:
                print("Voice callback error:", e)
