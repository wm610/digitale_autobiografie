class Raspberry:
    def __init__(self):
        button_start_recording = 0
        button_stop_recording = 0
        button_next_question = 0
        button_previous_question = 0
        button_power_on = 0


    def should_record_run(self) -> bool:
        return True

    def was_next_question_pressed(self) -> bool:
        return True

    def was_previous_question_pressed(self) -> bool:
        return True

    def is_power_button_on(self) -> bool:
        return True
