import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM (use GPIO numbers, not pin numbers)
GPIO.setmode(GPIO.BCM)

# Define button GPIO pin
BUTTON_PIN = 17  # Change this to your actual GPIO pin

# Set up the button as an input with a pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Press the button...")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button is pressed
            print("Button Pressed!")
            time.sleep(0.2)  # Debounce delay

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()  # Reset GPIO settings on exit