from arduino import Arduino 
from speach_processing import SpeachProcessing 
from ai import Ai
from ui import ErzaehlomatUI 
from pathlib import Path
import tkinter as tk
import setup
import time
# import sounddevice as sd
# import numpy as np
import speech_recognition as sr

class Controller:
    def __init__(self):
        # TODO This should be in an env file
        self.category_treshold = 10 # after this amount of questions the next category is 
        self.categories=["Base","Childhood/Family","Family","Job","Travel","Values"]
        
        self.logger = setup.get_logger()
        
        self.arduino = Arduino()
        self.logger.info(f"Start loading UI")
        self.ui = ErzaehlomatUI(tk.Tk())
        self.logger.info(f"Start loading Speach Processing")
        self.speach_processing = SpeachProcessing(self.arduino)
        self.logger.info(f"Start loading first AI")
        self.ai1 = Ai() # for summarising start questions to a profile
        self.logger.info(f"Start loading second AI")
        self.ai2 = Ai() # for generating new questions
        self.logger.info(f"Start loading third AI")
        self.ai3 = Ai() # maybe not here needed here

        self.questions : list[str] = self.create_start_questions()
        self.answers_txt : list[Path] = []
        self.answers_wav : list[Path] = []
        self.profiles : list[Path] = [] # this are the summaries of all categories + 1 base summaries
        self.current_question_index = 0 # points on the current question
        self.done_with_start_questions = False
        self.category_question_counter = 0 # counts the questions per category
        self.current_category_index = 0
        self.amout_of_categories = len(self.categories)
        self.recording = False
        self.audio_data = []
        self.samplerate = 48000 #Sample rate in Hz, 44100 on Windows
        self.current_directory = Path.cwd()
        self.recordings_path = self.current_directory / "recordings"
        self.textfiles_path = self.current_directory / "textfiles"
        # self.mic = sr.Microphone(self.samplerate) # for Martin
        self.mic = sr.Microphone(device_index=5) # for Benno
        self.recognizer = sr.Recognizer()

    def create_start_questions(self):
        return ["What is your name?", "How old are you?", "Where are you at home?"] # load questions from a file

    def check_question_already_recorded(self):
            #check if next question is already recorded
        existing_files = list(self.recordings_path.glob(f"{self.current_question_index}_*.wav"))
        if existing_files:
            self.ui.show_saved_frame()
        else:
            self.ui.hide_frame()
        #otherwise hide frame

    # def callback(self, indata, frames, time, status): ##had no time thinking about what this does but we need it for recording
    #     if status:
    #         print(status)
    #     self.audio_data.append(indata.copy())
        
    def start_audio_recording(self):
        # self.audio_data = []  # Reset data
        # self.recording = True
        self.recordings_path.mkdir(exist_ok=True)
        self.ui.show_recording_frame()
    #     with self.mic:
    #         while self.arduino.should_record_run():
    #             self.arduino.update_button_states()
    #             print("update_button_states")
    #             try:
    #                 self.recognizer.adjust_for_ambient_noise(self.mic, duration=1)
    #                 self.audio_data = self.recognizer.listen(self.mic, timeout=10)
    #             except self.arduino.was_next_question_pressed():
    #                 self.current_question_index += 1
    #                 self.update_question_in_ui()
    #                 self.check_question_already_recorded()
    #             except self.arduino.was_previous_question_pressed():
    #                 if self.current_question_index > 0: self.current_question_index -= 1
    #                 self.update_question_in_ui()
    #                 self.check_question_already_recorded()      
    #     print("Stop Record")
    #     self.stop_audio_recording(self.audio_data)
    
    # def stop_audio_recording(self, audio_data):
        # store wav file
        # if self.recording:
        self.recording = False
        self.ui.show_wait_frame()
        self.logger.info("start recording")
        filepath_wav : Path = self.speach_processing.create_wav_file(self.current_question_index,self.categories[self.current_category_index])
        self.logger.info("stopped recording")
        filepath_txt : Path = self.speach_processing.create_txt_file(filepath_wav,self.current_question_index,self.categories[self.current_category_index])
        self.answers_txt.append(filepath_txt)
        self.answers_wav.append(filepath_wav)
        self.ui.show_saved_frame()
    
    def update_question_in_ui(self):
        """
        generates a new question if current_question_index == len(questions)
        otherwise it displayes old questions
        """
        if self.current_question_index == len(self.questions):
            lower_bound : int = len(self.profiles) * self.category_treshold
            self.ui.show_wait_frame()
            new_generated_question = self.ai2.generate_new_question(self.profiles,
                                                                    self.questions[lower_bound:lower_bound+self.category_question_counter],
                                                                    self.answers_txt[lower_bound:lower_bound+self.category_question_counter],
                                                                    self.categories[self.current_category_index]) # only 

            self.ui.hide_frame()
            self.questions.append(new_generated_question)
            self.category_question_counter += 1
            if self.category_question_counter == self.category_treshold:
                # create new summary of the current category and append to profiles
                self.ui.show_wait_frame()
                self.ai1.generate_summary(self.questions[lower_bound:lower_bound+self.category_treshold], self.answers_txt[lower_bound:lower_bound:lower_bound+self.category_treshold])
                self.ui.hide_frame()
                self.category_question_counter = 0
                self.current_category_index += 1    #TODO solve bug if you move back to last category
        self.logger.info(f"New question: {self.questions[self.current_question_index]}")
        self.ui.update_question(self.questions[self.current_question_index])
        self.check_question_already_recorded()

    def execute_next_cmd(self):        
        self.arduino.update_button_states()

        # update the question only if next or previous question button were pressed
        if self.arduino.was_next_question_pressed():
            self.current_question_index += 1
            self.update_question_in_ui()
            self.check_question_already_recorded()
        elif self.arduino.was_previous_question_pressed():
            if self.current_question_index > 0:
                self.current_question_index -= 1
                self.update_question_in_ui()
                self.check_question_already_recorded()

        # start the recording if the user wants to run it
        if self.arduino.should_record_run():
            self.start_audio_recording()
        

    def start(self):
            
        self.update_question_in_ui() # display first question

        while not self.arduino.is_power_button_off():
            self.execute_next_cmd()

        see_you_msg = "Thank you for your time. See you next time."
        self.logger.info(f"New question: {see_you_msg}")
        self.ui.update_question(see_you_msg)

        time.sleep(5)


if __name__ == '__main__':
    controller : Controller = Controller()
    controller.start()