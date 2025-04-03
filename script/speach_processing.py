from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
from pathlib import Path

from arduino import Arduino
import speech_recognition as sr

# from pathlib import Path
# import numpy as np
# import scipy.io.wavfile as wav

class SpeachProcessing:
    def __init__(self, arduino : Arduino):
        self.THRESHOLD = 500
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100 # 48000

        self.arduino = arduino
        self.recognizer = sr.Recognizer()


        self.current_directory = Path.cwd()
        self.recordings_path = self.current_directory / "recordings"
        self.textfiles_path = self.current_directory / "textfiles"


    def create_wav_file(self, audio_data, current_question_index, current_category: str) -> Path:
        """
        take in audio data and return its path after saving
        """
        path = self.recordings_path / f"{current_question_index}_{current_category}.wav"

        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self.record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(str(path), 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()

        return path


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


    def is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        # return max(snd_data) < THRESHOLD
        return not self.arduino.should_record_run()

    def normalize(snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def trim(snd_data):
        "Trim the blank spots at the start and end"
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        silence = [0] * int(seconds * self.RATE)
        r = array('h', silence)
        r.extend(snd_data)
        r.extend(silence)
        return r

    def record(self):
        """
        Record a word or words from the microphone and 
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the 
        start and end, and pads with 0.5 seconds of 
        blank sound to make sure VLC et al can play 
        it without getting chopped off.
        """
        print("record")
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=1, rate=self.RATE,
            input=True, output=True,
            frames_per_buffer=self.CHUNK_SIZE)

        num_silent = 0
        snd_started = False

        r = array('h')

        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 30:
                break

        sample_width = p.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.5)
        return sample_width, r

    # def record_to_file(path):
    #     "Records from the microphone and outputs the resulting data to 'path'"
    #     sample_width, data = record()
    #     data = pack('<' + ('h'*len(data)), *data)

    #     wf = wave.open(path, 'wb')
    #     wf.setnchannels(1)
    #     wf.setsampwidth(sample_width)
    #     wf.setframerate(RATE)
    #     wf.writeframes(data)
    #     wf.close()

    # if __name__ == '__main__':
    #     print("please speak a word into the microphone")
    #     record_to_file('demo.wav')
    #     print("done - result written to demo.wav")