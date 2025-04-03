import speech_recognition as sr
from pathlib import Path
import numpy as np
import scipy.io.wavfile as wav
###Testing

class SpeachProcessing:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.current_directory = Path.cwd()
        self.recordings_path = self.current_directory / "recordings"
        self.textfiles_path = self.current_directory / "textfiles"
        self.samplerate = 48000 #Sample rate in Hz, 44100 on Windows
        self.audio_data=[]
 
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
        with sr.AudioFile(str(filepath_wav)) as source:
            audio_data = self.recognizer.record(source)  # Read the audio file
            try:
                self.textfiles_path.mkdir(exist_ok=True)
                textfilename = self.textfiles_path / f"{current_question_index}_{current_category}.txt"

                text = self.recognizer.recognize_google(audio_data, language="de-DE")
                with open(textfilename, "w") as file:
                    file.write(text)
                print("Transcription saved to output.txt")
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError:
                print("Error with the recognition service")

        return textfilename
    
    def audio_diagnostic_info(self):
        """Print diagnostic information about the audio input device using the speech_recognition library."""
        try:
            # Get the default microphone
            with sr.Microphone() as mic:
                device_index = mic.device_index
                print(f"Using audio input device index: {device_index}")
                print(f"Sample rate: {mic.SAMPLE_RATE} Hz")
                print(f"Chunk size: {mic.CHUNK} frames")
        except OSError as e:
            print(f"Error accessing the microphone: {e}")

    def callback(self, indata, frames, time, status): ##old function from sounddevice
        if status:
            print(status)
        self.audio_data.append(indata.copy())

def main():
    sp = SpeachProcessing()
    current_directory = Path.cwd()
    recordings_path = current_directory / "recordings"
    textfiles_path = current_directory / "textfiles"
    recordings_path.mkdir(exist_ok=True)  # Ensure the recordings folder exists
    recording = True
    # File path for the audio file
    audiofile_path = recordings_path / "test.wav"

    # Initialize the recognizer and microphone
    recognizer = sr.Recognizer()
    with sr.Microphone(sample_rate=48000) as mic:
        print("Recording... Press Ctrl+C to stop.")
        try:
            # Adjust for ambient noise and record audio
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            print("Start speaking...")
            while recording:
                audio_data = recognizer.listen(mic, timeout=None, phrase_time_limit=None)  # start audio record
            # Save the audio data to a WAV file
            with open(audiofile_path, "wb") as audio_file:
                audio_file.write(audio_data.get_wav_data())
            print(f"Audio saved to: {audiofile_path}")

            # Optionally, create a transcription
            sp.create_txt_file(audiofile_path, 42, "current_category")

        except KeyboardInterrupt:
            recording = False
            print("Recording stopped by user.")
        except Exception as e:
            recording = False
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()