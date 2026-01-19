import subprocess
import time
import ollama

SYSTEM_PROMPT = "You are MARKIS, a helpful AI assistant."

def start_ollama():
    subprocess.Popen(
        "ollama serve",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )
    for _ in range(10):
        try:
            ollama.Client().list()
            return
        except:
            time.sleep(0.5)

class ChatBot:
    def __init__(self, model="markis.v2.1"):
        start_ollama()
        self.client = ollama.Client()
        self.model = model
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def add_user(self, text):
        self.messages.append({"role": "user", "content": text})

    def add_ai(self, text):
        self.messages.append({"role": "assistant", "content": text})

    def stream(self):
        return self.client.chat(
            model=self.model,
            messages=self.messages,
            stream=True
        )
