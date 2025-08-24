from ultralytics import YOLO
from text_to_speech import TTSManager

model = YOLO('yolov8n.pt')
tts = TTSManager()

def detect_items(image_path="test_images/fishing.jpeg", save=False):

    #image_path = 'test_images/pizza.jpeg' # can either have pi store image in folder or pass it directly

    results = model(image_path)
    for result in results:
        for box in result.boxes:
            object_name = result.names[int(box.cls)]
            confidence = box.conf.item()
            print(f"Object: {object_name}, Confidence: {confidence:.2f}")
            tts.queue_object(object_name, confidence)
    
    if save:
        tts.save_queue_to_wav()
    else:
        tts.speak_queue()

