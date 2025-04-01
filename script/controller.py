from raspberry import Raspberry 
from speach_processing import SpeachProcessing 
from ai import Ai
from ui import ErzaehlomatUI 
from pathlib import Path
import tkinter as tk

class Controller:
    def __init__(self):
        self.ui = ErzaehlomatUI(tk.Tk())
        self.speach_processing = SpeachProcessing()
        self.ai1 = Ai() # for summarising start questions to a profile
        self.ai2 = Ai() # for generating new questions
        self.ai3 = Ai() # maybe not here needed here
        self.raspberry = Raspberry()

        self.questions : list[str] = self.create_start_questions()
        self.answers_txt : list[Path] = []
        self.answers_wav : list[Path] = []
        self.profiles : list[Path] = [] # this are the summaries of all categories + 1 base summaries
        self.current_question_index = 0 # points on the current question
        self.done_with_start_questions = False
        self.category_question_counter = 0 # counts the questions per category
        
        # TODO This should be in an env file
        self.category_treshold = 10 # after this amount of questions the next category is 
        self.amout_of_categories = 6

    def create_start_questions(self):
        return [] # load questions from a file

    def start_audio_recording(self):
        while self.raspberry.should_record_run():
            if self.raspberry.was_next_question_pressed():
                self.current_question_index += 1
                self.update_question_in_ui()
                break
            elif self.raspberry.was_previous_question_pressed():
                if self.current_question_index > 0: self.current_question_index -= 1
                self.update_question_in_ui()
                break        
        self.stop_audio_recording()
    
    def stop_audio_recording(self):
        # store wav file
        filepath_txt : Path = self.speach_processing.create_txt_file()
        filepath_wav : Path = self.speach_processing.create_wav_file()
        self.answers_txt.append(filepath_txt)
        self.answers_wav.append(filepath_wav)
    
    def update_question_in_ui(self):
        """
        generates a new question if current_question_index == len(questions)
        otherwise it displayes old questions
        """
        if self.current_question_index == len(self.questions):
            lower_bound : int = len(self.profiles) * self.category_treshold
            new_generated_question = self.ai2.generate_new_question(self.profiles,
                                                                    self.questions[lower_bound:lower_bound+self.category_question_counter],
                                                                    self.answers_txt[lower_bound:lower_bound+self.category_question_counter]) # only 

            self.questions.append(new_generated_question)
            self.category_question_counter += 1
            if self.category_question_counter == self.category_treshold:
                # create new summary of the current category and append to profiles
                self.ai1.generate_summary(self.questions[lower_bound:lower_bound+self.category_treshold], self.answers_txt[lower_bound:lower_bound:lower_bound+self.category_treshold])
                self.category_question_counter = 0
        self.ui.update_question(self.questions[self.current_question_index]) 

    def execute_next_cmd(self):        
        # update the question only if next and previous question button were pressed
        if self.raspberry.was_next_question_pressed():
            self.current_question_index += 1
            self.update_question_in_ui()
        elif self.raspberry.was_previous_question_pressed():
            if self.current_question_index > 0:
                self.current_question_index -= 1
                self.update_question_in_ui()

        # start the recording if the user wants to run it
        if self.raspberry.should_record_run():
            self.start_audio_recording()
        
            



    def start(self):
            
        self.update_question_in_ui() # display first question

        while self.raspberry.is_power_button_on():
            self.execute_next_cmd()

        self.ui.update_question("Thank you for your time. See you next time.")

        # shut raspberry off



if __name__ == '__main__':
    controller : Controller = Controller()
    controller.start()