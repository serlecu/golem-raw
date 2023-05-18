void setupRGBLED() {
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);    
}

// UTILITY FUNCTIONS ===============================

void inLedWhite(bool state) {
  if(state){
    digitalWrite(LEDR, !state);
    digitalWrite(LEDG, !state);
    digitalWrite(LEDB, !state);
  } else {
    digitalWrite(LEDR, state);
    digitalWrite(LEDG, state);
    digitalWrite(LEDB, state);
  }
}

void inLedRed(bool state) {
  if(state){
    digitalWrite(LEDR, !state);
    digitalWrite(LEDG, state);
    digitalWrite(LEDB, state);
  } else {
    digitalWrite(LEDR, !state);
  }
}
void inLedGreen(bool state) {
  if (state) {
  digitalWrite(LEDR, state);
  digitalWrite(LEDG, !state);
  digitalWrite(LEDB, state);
  } else {
    digitalWrite(LEDG, !state);
  }
}
void inLedBlue(bool state) {
  if (state) {
  digitalWrite(LEDR, state);
  digitalWrite(LEDG, state);
  digitalWrite(LEDB, !state);
  } else {
    digitalWrite(LEDB, !state);
  }
}
void readySequence(int loop = 2) {
  while (loop > 0) {
    inLedGreen(HIGH);
    delay(250);
    inLedBlue(HIGH);
    delay(250);
    loop --;
  }
  inLedBlue(LOW);
}
void errorSequence(int loop = 2) {
  while (loop > 0){
    inLedRed(HIGH);
    delay(250);
    inLedRed(LOW);
    delay(250);
    loop --;
  }
}

void blink(){
    led1 = !led1;
}
