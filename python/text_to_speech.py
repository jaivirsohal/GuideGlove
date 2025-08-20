import pyttsx3
import os

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = []
    
    def _check_empty(self):
        if not self.queue:
            self.queue.append("No items detected, please try again")

    def queue_object(self, name, confidence):
        text_to_speak = f"{name} with {confidence:.2f} confidence"
        self.queue.append(text_to_speak)

    def speak_queue(self):
        self._check_empty()
        text = ", ".join(self.queue)
        self.engine.say(text)
        self.engine.runAndWait()
        self.queue.clear()

    def save_queue_to_wav(self, filename='detected_objects.wav'):
        self._check_empty()
        directory = 'audio_output/'
        filepath = os.path.join(directory, filename)

        text = ", ".join(self.queue)
        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()

        self.queue.clear()
