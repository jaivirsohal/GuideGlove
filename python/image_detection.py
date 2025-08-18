from ultralytics import YOLO

model = YOLO('yolov8n.pt')
image_path = 'test_images/pizza.jpeg' # can either have pi store image in folder or pass it directly
results = model(image_path)
for result in results:
    for box in result.boxes:
        print(f"Object: {result.names[int(box.cls)]}, Confidence: {box.conf.item():.2f}")
        # to speak:
        # f"{result.names[int(box.cls)]} with {box.conf.item():.2f} confidence"