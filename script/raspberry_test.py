import time
import gpiod
import setup

class Raspberry:
    def __init__(self):
        self.logger = setup.get_logger()

        self.button_power_off = 5
        self.button_next_question = 6
        self.button_previous_question = 13
        self.button_stop_recording = 26
        self.button_start_recording = 29
        self.button_speak = 12

        self.chip = gpiod.Chip('gpiochip4')
        self.line_power_off = self.chip.get_line(self.button_power_off)
        self.line_next_question = self.chip.get_line(self.button_next_question)
        self.line_previous_question = self.chip.get_line(self.button_previous_question)
        self.line_stop_recording = self.chip.get_line(self.button_stop_recording)
        self.line_start_recording = self.chip.get_line(self.button_start_recording)
        self.line_speak = self.chip.get_line(self.button_speak)

        self.line_power_off.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
        self.line_next_question.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
        self.line_previous_question.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
        self.line_stop_recording.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
        self.line_start_recording.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
        self.line_speak.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)

        self.record_runs = False
        self.next_question = False
        self.previous_question = False
        self.power_off = False
        self.speak = False

    def update_button_states(self):
        state_power_off = self.line_power_off.get_value()
        state_next_question = self.line_next_question.get_value()
        state_previous_question = self.line_previous_question.get_value()
        state_stop_recording = self.line_stop_recording.get_value()
        state_start_recording = self.line_start_recording.get_value()
        state_speak = self.line_speak.get_value()

        self.logger(f"po={state_power_off}, nq={state_next_question}, pq={state_previous_question}, sta={state_start_recording}, sto={state_stop_recording}, sp={state_speak}")
        # if state_power_off == 1: 
        #     self.logger.info("button_power_off")
        #     self.power_off = True
        # if state_next_question == 1:
        #     self.logger.info("button_next_question")
        #     self.next_question = True
        # if state_previous_question == 1:
        #     self.logger.info("button_previous_question")
        #     self.previous_question = True
        # if state_start_recording == 1:
        #     self.logger.info("button_start_recording")
        #     self.record_runs = True
        # if state_stop_recording == 1:
        #     self.logger.info("button_stop_recording")
        #     self.record_runs = False
        # if state_speak == 1:
        #     self.logger.info("button_speak")
        #     self.speak = True


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
    def is_power_button_on(self) -> bool:
        return self.power_off
    def was_speak_pressed(self) -> bool:
        result = self.speak
        self.speak = False
        return result
    
    def release(self):
        self.line_power_off.release()
        self.line_next_question.release()
        self.line_previous_question.release()
        self.line_stop_recording.release()
        self.line_start_recording.release()
        self.line_speak.release()
                                

    
if __name__ == '__main__':
    raspberry : Raspberry = Raspberry()

    start_time = time.time()
    while time.time() - start_time < 30:
        raspberry.update_button_states()
        time.sleep(0.5)

    raspberry.release()