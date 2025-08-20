import pyttsx3

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = []

    def queue_object(self, name, confidence):
        text_to_speak = f"{name} with {confidence:.2f} confidence"
        self.queue.append(text_to_speak)

    def speak_queue(self):
        if not self.queue:
            self.queue.append("No items detected, please try again")
        self.engine.say(", ".join(self.queue))
        self.engine.runAndWait()
        self.queue.clear()