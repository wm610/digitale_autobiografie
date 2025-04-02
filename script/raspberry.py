import RPi.GPIO as GPIO
import setup

class Raspberry:
    def __init__(self):
        self.logger = setup.get_logger
        GPIO.setmode(GPIO.BCM) # GPIO Mode: BCM refers to GPIO numbering, BOARD refers to pin numbering

        button_start_recording = 17
        button_stop_recording = 27
        button_next_question = 22
        button_previous_question = 23
        button_power_off = 24
        led_power = 5
        led_recording = 6

        GPIO.setup(button_start_recording,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button_stop_recording,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button_next_question,     GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button_previous_question, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button_power_off,         GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(led_power,                GPIO.OUT)
        GPIO.setup(led_recording,            GPIO.OUT)

        GPIO.add_event_detect(button_start_recording,   GPIO.FALLING, callback=self.callback_start_recording,   bouncetime=200)
        GPIO.add_event_detect(button_stop_recording,    GPIO.FALLING, callback=self.callback_stop_recording,    bouncetime=200)
        GPIO.add_event_detect(button_next_question,     GPIO.FALLING, callback=self.callback_next_question,     bouncetime=200)
        GPIO.add_event_detect(button_previous_question, GPIO.FALLING, callback=self.callback_previous_question, bouncetime=200)
        GPIO.add_event_detect(button_power_off,         GPIO.FALLING, callback=self.callback_power_off,         bouncetime=200)

        self.record_runs = False
        self.next_question = False
        self.previous_question = False
        self.power_off = False
    
    def callback_start_recording(self, channel):
        self.logger.info("button_start_recording")
        self.record_runs = True
    def callback_stop_recording(self, channel):
        self.logger.info("button_stop_recording")
        self.record_runs = False
    def callback_next_question(self, channel):
        self.logger.info("button_next_question")
        self.next_question = True
    def callback_previous_question(self, channel):
        self.logger.info("button_previous_question")
        self.previous_question = True
    def callback_power_off(self, channel):
        self.logger.info("button_power_off")
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
    def is_power_button_on(self) -> bool:
        return self.power_off