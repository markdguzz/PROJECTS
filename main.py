from chatbot import ChatBot
from tts_engine import TTSEngine
from voice_input import VoiceInput
from gui_elements import GUI

VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"

def main():
    chatbot = ChatBot()
    tts = TTSEngine()
    voice = VoiceInput(VOSK_MODEL_PATH)

    gui = GUI(chatbot, tts, voice)
    gui.run()

if __name__ == "__main__":
    main()
