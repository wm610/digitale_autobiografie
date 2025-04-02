from pathlib import Path
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


class SpeachProcessing:
    def __init__(self):
        self.model_size = "small"
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="float32")
        self.recording = False
        self.audio_data = []
        self.samplerate = 48000 #Sample rate in Hz, 44100 on Windows

    def create_txt_file(self, wav_file_path) -> Path:
        segments = self.model.transcribe(wav_file_path, beam_size=5, vad_filter=True)
        with open(Path.home, 'w', encoding='utf-8') as file:
            for segment in segments:
                file.write(f"{segment.text}\n")
        
        return Path.home()
    
    def create_wav_file(self) -> Path:
        
        return Path.home()
    
    def audio_diagnostic_info():
        """Print diagnostic information about the audio input device."""
        default_device = sd.default.device[0]  # Index of the default input device
        device_info = sd.query_devices(default_device)  # Get device details
        print(f"Using audio input device: {device_info['name']}")
        print(f"Sample rate: {device_info['default_samplerate']} Hz")
        print(f"Channels: {device_info['max_input_channels']}")
        print("Press 's' to start recording and 'e' to stop.")