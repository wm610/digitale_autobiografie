from gpiozero import Button
from signal import pause

# Define button connected to GPIO 17
button = Button(17)

# Function to run when button is pressed
def button_pressed():
    print("Button Pressed!")

# Attach event listener
button.when_pressed = button_pressed

print("Waiting for button press...")
pause()  # Keeps the program running