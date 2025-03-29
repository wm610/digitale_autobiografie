import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import keyboard  # For detecting key presses

# Get default input device
default_device = sd.default.device[0]  # Index of the default input device
device_info = sd.query_devices(default_device)  # Get device details

# Print device information
print(f"Using audio input device: {device_info['name']}")
print(f"Sample rate: {device_info['default_samplerate']} Hz")
print(f"Channels: {device_info['max_input_channels']}")

# Recording settings
samplerate = 44100  # Sample rate in Hz
filename = "C:/Users/marti/Documents/Programmieren/DigitaleAutobiografie/recordings/recording.wav"

audio_data = []
recording = False  # Flag to track recording state

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_data.append(indata.copy())

def start_recording():
    global recording, audio_data
    if not recording:
        print("Recording started... Press 'e' to stop.")
        audio_data = []  # Reset data
        recording = True
        with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, dtype=np.int16):
            keyboard.wait("e")  # Wait for 'e' to stop recording

        stop_recording()

def stop_recording():
    global recording
    if recording:
        recording = False
        print("Recording stopped.")

        # Convert list to numpy array and save
        audio_data_np = np.concatenate(audio_data, axis=0)
        wav.write(filename, samplerate, audio_data_np)
        print(f"Saved as {filename}")

print("Press 's' to start recording and 'e' to stop.")

while True:
    keyboard.wait("s")  # Wait for 's' key to start recording
    start_recording()