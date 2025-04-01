import raspberry
import speach_processing
import ai
from pathlib import Path

class Controller:
    def __init__(self):
        ui = UI()
        speach_to_text = SpeachToText()
        ai1 = AI() # for summarising start questions to a profile
        ai2 = AI() # for generating new questions
        ai3 = AI() # maybe not here needed here
        raspberry = Raspberry()

        questions : list[str] = self.create_start_questions()
        answers_txt : list[Path] = []
        answers_wav : list[Path] = []
        profiles : list[Path] = [] # this are the summaries of all categories + 1 base summaries
        current_question_index = 0
        done_with_start_questions = False
        category_question_counter = 0 # counts the questions per category
        
        # TODO This should be in an env file
        category_treshold = 10 # after this amount of questions the next category is 
        amout_of_categories = 6

    def create_start_questions(self):
        return [] # load questions from a file

    def start_audio_recording(self):
        while raspberry.should_record_run():
            if raspberry.was_next_question_pressed():
                self.current_question_index += 1
                self.update_question_in_ui()
                break
            elif raspberry.was_previous_question_pressed():
                if self.current_question_index > 0: self.current_question_index -= 1
                self.update_question_in_ui()
                break        
        self.stop_audio_recording()
    
    def stop_audio_recording(self):
        # store wav file
        filepath_txt : Path = self.speach_to_text.create_txt_file()
        filepath_wav : Path = self.speach_to_text.create_wav_file()
        self.answers_txt.append(filepath_txt)
        self.answers_wav.append(filepath_wav)
    
    def update_question_in_ui(self):
        """
        generates a new question if current_question_index == len(questions)
        otherwise it displayes old questions
        """
        if self.current_question_index == len(self.questions):
            new_generated_question = self.ai2.generate_new_question(self.profiles,
                                                                                           self.category_question_counter, 
                                                                                           self.questions[category_question_counter:category_question_counter],
                                                                                           self.answers_txt[category_question_counter:category_question_counter]) # only 
            # this function needs to consider all the generated problems as well as the last x questions of this category
            # it returns the new question and the new counter
            self.question.append(new_generated_question)
            self.category_question_counter += 1
            if self.category_question_counter == self.category_treshold:
                # create new summary of the current category and append to profiles
                self.ai1.generate_summary(self.questions[category_question_counter:category_question_counter], self.answers_txt[category_question_counter:category_question_counter])
                self.category_question_counter = 0
        self.ui.update_question(self.questions[self.current_question_index]) 

    def execute_next_cmd(self):        
        # update the question only if next and previous question button were pressed
        if raspberry.was_next_question_pressed():
            self.current_question_index += 1
            self.update_question_in_ui()
        elif raspberry.was_previous_question_pressed():
            if self.current_question_index > 0:
                self.current_question_index -= 1
                self.update_question_in_ui()

        # start the recording if the user wants to run it
        if raspberry.should_record_run():
            self.start_audio_recording()
        
            



    def start(self):
            
        self.update_question_in_ui() # display first question

        while raspberry.is_power_button_on():
            self.execute_next_cmd()

        self.ui.update_question("Thank you for your time. See you next time.")

        # shut raspberry off



if __name__ == '__main__':
    controller : Controller = Controller()
    controller.start()