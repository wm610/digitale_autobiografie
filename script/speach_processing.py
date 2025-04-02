from pathlib import Path
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


class SpeachProcessing:
    def __init__(self):
        self.model_size = "small"
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="float32")
        self.current_directory = Path.cwd()
        self.recordings_path = self.current_directory / "recordings"
        self.textfiles_path = self.current_directory / "textfiles"
        self.samplerate = 48000 #Sample rate in Hz, 44100 on Windows
 
    def create_wav_file(self, audio_data, current_question_index, current_category: str) -> Path:
        """
        take in audio data and return its path after saving
        """
        audio_data_np = np.concatenate(audio_data, axis=0)
        filename = self.recordings_path / f"{current_question_index}_{current_category}.wav"
        wav.write(filename, self.samplerate, audio_data_np)
        return filename

    def create_txt_file(self, filepath_wav, current_question_index, current_category :str) -> Path:
        """
        take in audio data path, create transcription and return textfile path 
        """
        self.textfiles_path.mkdir(exist_ok=True)
        textfilename = self.textfiles_path / f"{current_question_index}_{current_category}.txt"
        segments = self.model.transcribe(filepath_wav, beam_size=5, vad_filter=True)
        with open(textfilename, 'w', encoding='utf-8') as file:
            for segment in segments:
                file.write(f"{segment.text}\n")
        return textfilename
    
    def audio_diagnostic_info(self):
        """Print diagnostic information about the audio input device."""
        default_device = sd.default.device[0]  # Index of the default input device
        device_info = sd.query_devices(default_device)  # Get device details
        print(f"Using audio input device: {device_info['name']}")
        print(f"Sample rate: {device_info['default_samplerate']} Hz")
        print(f"Channels: {device_info['max_input_channels']}")