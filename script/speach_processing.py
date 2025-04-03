from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import Controller

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from pathlib import Path
import speech_recognition as sr
from arduino import Arduino
import setup

from ui import ErzaehlomatUI
import tkinter as tk

# from pathlib import Path
# import numpy as np
# import scipy.io.wavfile as wav

class SpeachProcessing:
    def __init__(self, arduino : Arduino, controller : Controller, ui: ErzaehlomatUI):
        self.THRESHOLD = 500
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100 # 48000

        self.arduino = arduino
        self.controller = controller
        self.recognizer = sr.Recognizer()
        self.logger = setup.get_logger()

        self.current_directory = Path.cwd()
        self.recordings_path = self.current_directory / "recordings"
        self.textfiles_path = self.current_directory / "textfiles"

        self.ui = ui

    def create_wav_file(self, current_question_index, current_category: str) -> Path:
        """
        take in audio data and return its path after saving
        Records from the microphone and outputs the resulting data to 'path'
        """
        path = self.recordings_path / f"{current_question_index}_{current_category}.wav"

        self.logger.info(f"created wav file: {path}")
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
                self.logger.info(f"Transcription saved to {textfilename}")
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError:
                print("Error with the recognition service")

        return textfilename


    def should_stop(self, snd_data):
        # """Returns 'True' if recording should be stopped"""
        # self.logger.info("should_stop!!!!")
        # # return True
        #  self.arduino.update_button_states()
        if not self.arduino.should_record_run():
            return True
        elif self.arduino.was_next_question_pressed():
            self.controller.current_question_index += 1
            self.controller.update_question_in_ui(True)
            self.controller.check_question_already_recorded()
            return True
        elif self.arduino.was_previous_question_pressed():
            if self.controller.current_question_index > 0: self.current_question_index -= 1
            self.controller.update_question_in_ui(True)
            self.controller.check_question_already_recorded()
            return True
        else:
            return False

        # "Returns 'True' if below the 'silent' threshold"
        # return max(snd_data) < self.THRESHOLD

    def normalize(self, snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def trim(self, snd_data):
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
        p = pyaudio.PyAudio()
        self.ui.show_recording_frame()
        stream = p.open(format=self.FORMAT, channels=1, rate=self.RATE,
            input=True, output=True,
            frames_per_buffer=self.CHUNK_SIZE)
        # DEVICE_INDEX = 1  # find out your index with: "arecord -l" then use card number from the USB device 
        # stream = p.open(format=self.FORMAT, channels=2, rate=self.RATE,
        #     input=True, output=True, input_device_index=DEVICE_INDEX,
        #     frames_per_buffer=self.CHUNK_SIZE)

        num_silent = 0
        snd_started = False

        r = array('h')

        while 1:
        # while not self.should_stop():
            # little endian, signed short
            snd_data = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.should_stop(snd_data)

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
        self.ui.show_saved_frame()
        return sample_width, r

if __name__ == '__main__':
    from controller import Controller
    controller = Controller()
    arduino = Arduino()
    ui = ErzaehlomatUI(tk.Tk())
    speach_processing = SpeachProcessing(arduino=arduino, controller=controller, ui=ui)
    print("please speak a word into the microphone")
    file = speach_processing.create_wav_file(42, "current_category")
    print("done recording written to: {file}")