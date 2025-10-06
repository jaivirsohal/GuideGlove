# File: python/tempmain.py

import time
import image_detection
from picamera2 import Picamera2

# --- Configuration ---
IMAGE_FILEPATH = "python/test_images/capture.jpeg"

def take_photo(filepath):
    """Captures a photo using the Raspberry Pi Camera Module."""
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (1280, 720)})
    picam2.configure(config)

    print("Starting camera for capture...")
    picam2.start()
    time.sleep(2)  # Allow sensor to adjust

    try:
        picam2.capture_file(filepath)
        print(f"Photo saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error capturing photo: {e}")
        return False
    finally:
        picam2.stop()
        print("Camera stopped.")

def main():
    """
    Waits for a console command to trigger the detection process.
    This simulates the button press for easy testing.
    """
    print("GuideGlove Test Control is running.")
    
    while True:
        try:
            # Wait for the user to press Enter.
            # You could change this to `if input(...) == 'yes':` if you prefer.
            input("\n--- Press Enter to start identification (or Ctrl+C to exit) ---")
            
            print("\n--- Trigger received! Starting identification process... ---")
            
            # 1. Take a photo
            if take_photo(IMAGE_FILEPATH):
                # 2. Run object detection
                print("Running object detection...")
                image_detection.detect_items(IMAGE_FILEPATH, save=False)
            else:
                print("Could not run detection because photo capture failed.")
            
            print("--- Process complete. Ready for next command. ---")

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting.")
            break

if __name__ == '__main__':
    main()
