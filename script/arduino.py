import serial
import time
import setup

class Arduino:
    def __init__(self):

        # Make sure to install pyserial first:
        # pip install 

        # Configure the serial port
        self.ser = serial.Serial('/dev/ttyACM0', 4800, timeout=1) # 9600
        self.ser.flush()

        self.logger = setup.get_logger()

        self.record_runs = False
        self.next_question = False
        self.previous_question = False
        self.power_off = False
        self.speak = False

        self.current_button_state : str = "000000"
        self.number_of_buttons = len(self.current_button_state)
        self.pressed_buttons = [False for _ in range(self.number_of_buttons)]

    def update_button_states_thread(self, stop_event):
        while not stop_event.is_set():
            self.update_button_states()
        self.logger.info("Arduino Thread stopping...")

    def update_button_states(self):
        self.logger.debug(f"{self.current_button_state}")
        try:
            if self.ser.in_waiting > 0:
                self.current_button_state = self.ser.read(self.ser.in_waiting).decode('utf-8').rstrip()
        except KeyboardInterrupt:
            print("\nExiting program")
            self.ser.close()

        for i in range(self.number_of_buttons):
            if self.current_button_state[i] == '1' and not self.pressed_buttons[i]:
                self.pressed_buttons[i] = True
            if self.current_button_state[i] == '0' and self.pressed_buttons[i]:
                self.pressed_buttons[i] = False
                self.update_internal_states(i)
    
    def update_internal_states(self, i):
        if 0 == i:
            self.logger.info(f"START RECORDING pressed")
            self.record_runs = True
        elif 1 == i:
            self.logger.info(f"STOP RECORDING pressed")
            self.record_runs = False
        elif 2 == i:
            self.logger.info(f"PREVIOUS QUESTION pressed")
            self.previous_question = True
        elif 3 == i:
            self.logger.info(f"NEXT QUESTION pressed")
            self.next_question = True
        elif 4 == i:
            self.logger.info(f"READ QUESTION pressed")
            self.speak = True
        elif 5 == i:
            self.logger.info(f"POWER OFF pressed")
            self.power_off = True

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
    
if __name__ == '__main__':
    arduino : Arduino = Arduino()

    start_time = time.time()
    while time.time() - start_time < 60:
        arduino.update_button_states()
