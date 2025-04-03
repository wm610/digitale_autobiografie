const int buttonPins[] = {2, 3, 4, 5, 6, 7};  // Connect buttons to these pins
const int numButtons = 6;

void setup() {
  Serial.begin(4800);
  for (int i = 0; i < numButtons; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);  // Use internal pull-up resistors
  }
}

void loop() {
  String buttonStates = "";
  
  for (int i = 0; i < numButtons; i++) {
    bool buttonPressed = !digitalRead(buttonPins[i]);  // Inverted because of pull-up
    buttonStates += buttonPressed ? "1" : "0";
  }
  
  Serial.println(buttonStates);
  delay(10);  // Small delay to avoid flooding the serial port
}