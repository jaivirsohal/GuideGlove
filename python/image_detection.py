from ultralytics import YOLO
import pyttsx3
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

model = YOLO('yolov8n.pt')
image_path = 'test_images/pizza.jpeg' # can either have pi store image in folder or pass it directly

def get_distance():
    """Reads the distance from the distances.txt file."""
    try:
        with open("../c/distances.txt", "r") as f:
            distance_str = f.readline().strip()
            return float(distance_str)
    except (IOError, ValueError):
        return -1.0

results = model(image_path)
for result in results:
    for box in result.boxes:
        object_name = result.names[int(box.cls)]
        confidence = box.conf.item()
        print(f"Object: {object_name}, Confidence: {confidence:.2f}")

        distance = get_distance()

        if distance >= 0:
            text_to_speak = f"{object_name} detected at {distance} centimeters with {confidence:.2f} confidence"
        else:
            text_to_speak = f"{object_name} with {confidence:.2f} confidence"


        # Make the engine speak the text
        engine.say(text_to_speak)
        engine.runAndWait()