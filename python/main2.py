import RPi.GPIO as GPIO
import time
import image_detection
from picamera2 import Picamera2
import os

# --- Configuration ---
BUTTON_PIN = 15  # GPIO pin the button is connected to (Broadcom numbering)
# Ensure the path is correct relative to this script's location
IMAGE_FILEPATH = "test_images/capture.jpeg"

# --- Global State Management ---
is_busy = False
picam2 = Picamera2()  # Create the camera object ONCE, here.

def take_photo(camera_obj, filepath):
    """
    Captures a photo using a pre-initialized and running camera object.
    """
    try:
        # The camera is already running, so we just capture the file.
        camera_obj.capture_file(filepath)
        print(f"Photo saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error capturing photo: {e}")
        return False

def identify_objects_callback(channel):
    """
    This function is called when the button is pressed.
    It handles the complete detection process and manages the busy state.
    """
    global is_busy

    # If the system is already busy, ignore the button press.
    if is_busy:
        print("\nSystem busy. Please wait for the current process to finish.")
        return

    # --- Start of process, set system to busy ---
    is_busy = True
    print("\n--- Button Pressed! Starting identification process... ---")

    # 1. Take a photo using the global camera object
    if take_photo(picam2, IMAGE_FILEPATH):
        # 2. Run object detection
        print("Running object detection...")
        # Make sure the image_detection script uses the same path
        image_detection.detect_items(IMAGE_FILEPATH, save=False)
    else:
        print("Could not run detection because photo capture failed.")

    print("--- Process complete. Ready for next command. ---")
    # --- End of process, release the busy flag ---
    is_busy = False

def main():
    """Sets up camera, GPIO and waits for button presses."""
    try:
        # --- Camera Setup ---
        print("Configuring camera...")
        config = picam2.create_still_configuration(main={"size": (1280, 1980)})
        picam2.configure(config)
        picam2.start()
        print("Camera started. Allowing 2 seconds for sensor to settle...")
        time.sleep(2)
        print("Camera ready.")

        # --- GPIO Setup ---
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
                              callback=identify_objects_callback,
                              bouncetime=1000) # Increased bouncetime to 1 sec

        print(f"GuideGlove Main Control is running.")
        print(f"Waiting for button press on GPIO {BUTTON_PIN}...")

        # Keep the script alive to listen for events
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up...")
    finally:
        # --- Cleanup ---
        picam2.stop()
        print("Camera stopped.")
        GPIO.cleanup()
        print("GPIO cleanup complete. Exiting.")

if __name__ == '__main__':
    # Make sure the test_images directory exists
    if not os.path.exists("test_images"):
        os.makedirs("test_images")
    main()
