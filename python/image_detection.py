from ultralytics import YOLO
import text_to_speech

model = YOLO('yolov8n.pt')

def detect_items(image_path="test_images/fishing.jpeg"):

    #image_path = 'test_images/pizza.jpeg' # can either have pi store image in folder or pass it directly

    results = model(image_path)
    for result in results:
        for box in result.boxes:
            object_name = result.names[int(box.cls)]
            confidence = box.conf.item()
            print(f"Object: {object_name}, Confidence: {confidence:.2f}")
            text_to_speech.queue_object(object_name, confidence)

    text_to_speech.speak_queue()

