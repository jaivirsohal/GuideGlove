import image_detection
import cv2

PHONE = 0 #these indices are for running on a mac
LAPTOP = 1
OTHER = 2

def take_photo(filepath, camera_index=PHONE):
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False
    
    #need to let the shutter open so take the 5th frame
    for _ in range(5):
        ret, frame = cap.read()
    
    cap.release()
    
    if ret:
        cv2.imwrite(filepath, frame)
        print(f"Photo saved to {filepath}")
        return True
    else:
        print("Error: Failed to capture photo")
        return False

filepath = "test_images/capture.jpeg"
if take_photo(filepath):
    image_detection.detect_items(filepath, save=False)