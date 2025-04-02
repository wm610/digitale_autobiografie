import time
import gpiod
import setup

class Raspberry:
    def __init__(self):
        self.logger = setup.get_logger()

        self.record_runs = False
        self.next_question = False
        self.previous_question = False
        self.power_off = False
        self.speak = False

        self.button_start_recording = 26
        self.button_stop_recording = 19
        self.button_previous_question = 13
        self.button_next_question = 6
        self.button_power_off = 5
        self.button_speak = 12

        try:
            self.chip = gpiod.Chip('gpiochip0')
        except FileNotFoundError:
            self.logger.error("GPIO chip not found: This system may not be a Raspberry Pi or you didn't run this file as root or you haven't installed the neccessary libraries")
            self.chip = None
            return

        self.line_start_recording = self.chip.get_line(self.button_start_recording)
        self.line_stop_recording = self.chip.get_line(self.button_stop_recording)
        self.line_previous_question = self.chip.get_line(self.button_previous_question)
        self.line_next_question = self.chip.get_line(self.button_next_question)
        self.line_power_off = self.chip.get_line(self.button_power_off)
        self.line_speak = self.chip.get_line(self.button_speak)

        self.line_start_recording.request(consumer="Button",    type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
        self.line_stop_recording.request(consumer="Button",     type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
        self.line_previous_question.request(consumer="Button",  type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
        self.line_next_question.request(consumer="Button",      type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
        self.line_power_off.request(consumer="Button",          type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
        self.line_speak.request(consumer="Button",              type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)


    def update_button_states(self):
        if self.chip == None:
            return

        state_start_recording = self.line_start_recording.get_value()
        state_stop_recording = self.line_stop_recording.get_value()
        state_previous_question = self.line_previous_question.get_value()
        state_next_question = self.line_next_question.get_value()
        state_power_off = self.line_power_off.get_value()
        state_speak = self.line_speak.get_value()

        self.logger.info(f"sta={state_start_recording}, sto={state_stop_recording}, pqe={state_previous_question}, nqe={state_next_question}, pof={state_power_off}, spe={state_speak}")
        if state_start_recording == 1:
            if self.record_runs != True: self.logger.info(f"START RECORDING pressed")
            self.record_runs = True
        if state_stop_recording == 1:
            if self.record_runs != False: self.logger.info(f"STOP RECORDING pressed")
            self.record_runs = False
        if state_previous_question == 1:
            if self.previous_question != True: self.logger.info(f"PREVIOUS QUESTION pressed")
            self.previous_question = True
        if state_next_question == 1:
            if self.next_question != True: self.logger.info(f"NEXT QUESTION pressed")
            self.next_question = True
        if state_power_off == 1:
            if self.power_off != True: self.logger.info(f"POWER OFF pressed")
            self.power_off = True
        if state_speak == 1:
            if self.speak != True: self.logger.info(f"READ QUESTION pressed")
            self.speak = True


    def should_record_run(self) -> bool:
        return self.record_runs
    def was_next_question_pressed(self) -> bool:
        result = self.next_question
        self.next_question = False
        return result
    def was_previous_question_pressed(self) -> bool:
        result = self.previous_question
        self.previous_question = False
        return result
    def is_power_button_off(self) -> bool:
        return self.power_off
    def was_speak_pressed(self) -> bool:
        result = self.speak
        self.speak = False
        return result
    
    def release(self):
        if self.chip == None:
            return
        
        self.line_power_off.release()
        self.line_next_question.release()
        self.line_previous_question.release()
        self.line_stop_recording.release()
        self.line_start_recording.release()
        self.line_speak.release()
                                

    
if __name__ == '__main__':
    raspberry : Raspberry = Raspberry()

    start_time = time.time()
    while time.time() - start_time < 60:
        raspberry.update_button_states()
        time.sleep(0.25)

    raspberry.release()