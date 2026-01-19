import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

class GUI:
    def __init__(self, chatbot, tts, voice):
        self.chatbot = chatbot
        self.tts = tts
        self.voice = voice

        self.root = tk.Tk()
        self.root.title("MARKBOT")
        self.root.geometry("720x820")

        # Chat display
        self.chat = ScrolledText(self.root, wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Input frame
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10)

        self.entry = tk.Entry(frame, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 8))
        self.entry.bind("<Return>", self.send_text)

        self.send_btn = tk.Button(frame, text="Send", command=self.send_text)
        self.send_btn.pack(side=tk.RIGHT)

        # Push-to-Talk button
        self.ptt_btn = tk.Button(self.root, text="🎙 Push To Talk", height=2)
        self.ptt_btn.pack(fill=tk.X, padx=10, pady=10)

        # Bind PTT
        self.ptt_btn.bind("<ButtonPress-1>", self.start_voice)
        self.ptt_btn.bind("<ButtonRelease-1>", self.stop_voice)

        # Connect voice input callback
        self.voice.on_result = self.receive_voice

        self.chat.insert(tk.END, "MARKBOT initialized.\nHold Push-To-Talk to speak.\n\n")

    # ---------------------------
    # Push-to-Talk callbacks
    # ---------------------------
    def start_voice(self, event):
        self.voice.start()

    def stop_voice(self, event):
        self.voice.stop()

    def receive_voice(self, text):
        # This is GUI-safe (called from root.after in voice_input)
        self.root.after(0, lambda: self.process_user(text, use_voice=True))

    # ---------------------------
    # Keyboard input
    # ---------------------------
    def send_text(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.process_user(text, use_voice=False)

    # ---------------------------
    # Process user input (voice or keyboard)
    # ---------------------------
    def process_user(self, text, use_voice):
        self.entry.delete(0, tk.END)
        self.chat.insert(tk.END, f"You: {text}\n\n")
        self.chat.see(tk.END)

        # Add user message
        self.chatbot.add_user(text)
        self.send_btn.config(state=tk.DISABLED)

        # Start AI response in a separate thread
        threading.Thread(target=self.stream_ai, args=(use_voice,), daemon=True).start()

    # ---------------------------
    # Stream AI response
    # ---------------------------
    def stream_ai(self, use_voice):
        self.chat.after(0, lambda: self.chat.insert(tk.END, "MARKIS: "))
        response = ""

        for chunk in self.chatbot.stream():
            token = chunk["message"]["content"]
            response += token
            # Append token to chat safely
            self.chat.after(0, lambda t=token: self.append(t))

        # Finish response
        self.chat.after(0, lambda: self.finish(response, use_voice))

    # ---------------------------
    # Append token
    # ---------------------------
    def append(self, token):
        self.chat.insert(tk.END, token)
        self.chat.see(tk.END)

    # ---------------------------
    # Finish AI response
    # ---------------------------
    def finish(self, text, use_voice):
        self.chat.insert(tk.END, "\n\n")
        self.chatbot.add_ai(text)
        self.send_btn.config(state=tk.NORMAL)

    # Trigger TTS ONLY if this was a voice prompt
        if use_voice:
            self.tts.speak(text)
    # ---------------------------
    # Start GUI main loop
    # ---------------------------
    def run(self):
        self.root.mainloop()
