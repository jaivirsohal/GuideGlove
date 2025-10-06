# File: python/main.py

import RPi.GPIO as GPIO
import time
import image_detection
from picamera2 import Picamera2

# --- Configuration ---
BUTTON_PIN = 15  # GPIO pin the button is connected to (Broadcom numbering)
IMAGE_FILEPATH = "test_images/capture.jpeg"

# --- State Management ---
# This global flag prevents new detections from starting while one is running.
is_busy = False

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

    # 1. Take a photo
    if take_photo(IMAGE_FILEPATH):
        # 2. Run object detection
        print("Running object detection...")
        image_detection.detect_items(IMAGE_FILEPATH, save=False)
    else:
        print("Could not run detection because photo capture failed.")

    print("--- Process complete. Ready for next command. ---")
    # --- End of process, release the busy flag ---
    is_busy = False

def main():
    """Sets up GPIO and waits for button presses."""
    try:
        # --- GPIO Setup ---
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
        # Setup the button pin with an internal pull-up resistor.
        # This means the pin is HIGH by default and goes LOW when pressed.
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Add an event detector for a falling edge (press), with debouncing.
        # 'bouncetime=500' means to ignore further presses for 0.5 seconds.
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, 
                              callback=identify_objects_callback, 
                              bouncetime=500)

        print("GuideGlove Main Control is running.")
        print(f"Waiting for button press on GPIO {BUTTON_PIN}...")
        
        # Keep the script alive to listen for events
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up...")
    finally:
        GPIO.cleanup()  # Clean up GPIO channels on exit
        print("GPIO cleanup complete. Exiting.")

if __name__ == '__main__':
    main()
