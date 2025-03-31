class Controller:
    def __init__(self):
        ui = UI()
        speach_to_text = speachToText()
        ai1 = AI()
        ai2 = AI()
        ai3 = AI() # maybe not here needed here
        button_start_recording
        button_stop_recording
        button_next_question
        button_last_question
        button_power_on

        record_active : bool = 

        start_questions : list[str] = create_start_questions()
        generated_questions : list[str] = []

    # question iterator
    def create_question_iterator():
        

    def start_audio_recording(question_name):
        while record_active:
        return audio_filename
        

    def start(self):
        question_iter = ()
        for question in start_questions:
            ui.update_question(question)
            if record_active:
                audio_filename = record_audio(question_name)
            answer_filename = speach_to_text.generate_txt(audio_filename)
        profile : str = ai1.create_profile()

        while not button_stop:
            last_three_answers = get_last_three_answers()
            question = get_new_question(last_three_answers, profile)


            













if __name__ == '__main__':
    controller : Controller = Controller()
    controller.start()