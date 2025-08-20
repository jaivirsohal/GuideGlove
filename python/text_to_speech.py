import pyttsx3

engine = pyttsx3.init()
queue = []

def queue_object(name, confidence):
    text_to_speak = f"{name} with {confidence:.2f} confidence"
    queue.append(text_to_speak)

def speak_queue():
    if not queue:
        queue.append("No items detected, please try again")
    engine.say(", ".join(queue))
    engine.runAndWait()
    queue.clear()