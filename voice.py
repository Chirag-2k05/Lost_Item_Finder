import speech_recognition as sr
import pyttsx3
import threading

recognizer = sr.Recognizer()

def speak_async(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    thread = threading.Thread(target=run)
    thread.start()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except:
            return None