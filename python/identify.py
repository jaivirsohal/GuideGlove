import image_detection
from picamera2 import Picamera2
import time

def take_photo(filepath):
    """
    Captures a photo using the Raspberry Pi Camera Module
    and saves it to the specified filepath.
    """
    picam2 = Picamera2()

    # Configure for a still image capture
    config = picam2.create_still_configuration(main={"size": (1920, 1920)})
    picam2.configure(config)

    print("Starting camera...")
    picam2.start()
    # Allow 3 seconds for auto-focus and auto-exposure to settle
    time.sleep(3)

    try:
        # The capture_file method saves the image directly
        picam2.capture_file(filepath)
        print(f"Photo saved to {filepath}")
        success = True
    except Exception as e:
        print(f"Error capturing photo: {e}")
        success = False
    finally:
        # Always ensure the camera is stopped
        picam2.stop()
        
    return success

# Define the output path relative to the project root
filepath = "python/test_images/capture.jpeg"

# Take a photo and then run detection on it
if take_photo(filepath):
    print("Running object detection...")
    image_detection.detect_items(filepath, save=False)
else:
    print("Could not run detection because photo capture failed.")
