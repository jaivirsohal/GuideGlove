import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set up BCM pin 18 as an input with a pull-up resistor
# The pull-up resistor means the pin will be HIGH by default
# and will go LOW when the button is pressed (connected to ground)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Button test started. Press the button. Press Ctrl+C to exit.")

try:
    while True:
        # Read the state of the button
        button_state = GPIO.input(15)

        # The button is pressed if the input is LOW
        if button_state == GPIO.LOW:
            print("Button Pressed")
            # Wait for a short period to avoid multiple rapid readings
            time.sleep(0.2)
        
        time.sleep(0.01) # A small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clean up the GPIO settings
    GPIO.cleanup()
