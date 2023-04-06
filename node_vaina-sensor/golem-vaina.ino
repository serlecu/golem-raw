#include <ArduinoBLE.h>
#include "Arduino_BMI270_BMM150.h" // Inertial Measurement Unit
#include <Arduino_APDS9960.h> // Digital proximity and ambient light as well as for detecting RGB colors and gestures.
#include <Arduino_HS300x.h> // Temperature and humidty
#include <Arduino_LPS22HB.h> // Barometric pressure
#include <PDM.h> // Pulse-density modulation microphones
// Check #include <ArduinoSound.h>

BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // create a custom service
//Magnet
BLEUnsignedCharCharacteristic BMMagChar("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//Color
BLEUnsignedCharCharacteristic apdColorChar("19B10002-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//Lux
BLEIntCharacteristic adpLuxChar("19B10003-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//Proximity
BLEUnsignedCharCharacteristic adpProxChar("19B10004-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//Temperature
BLEUnsignedCharCharacteristic hs3TempChar("19B10005-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//Humidity
BLEUnsignedCharCharacteristic hs3HumChar("19B10006-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//Presure
BLEUnsignedCharCharacteristic lpsPressChar("19B10007-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic
//IR
//BLEUnsignedCharCharacteristic customChar("19B10008-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic


// Mains
bool isConnected = false;
bool waitBleLed = false; //Blue Blink while waiting for connection
unsigned long disconnectedTimer;
unsigned long mainTimer;

// BMI270 & BMM150
int valAccelX, valAccelY, valAccelZ;
int valGyroX, valGyroY, valGyroZ;
float valMagnetX, valMagnetY, valMagnetZ;
// APD
int valColorR, valColorG, valColorB;
int valLight;
int valProximity;
// HS300x
int valTemperature, valHumidity;
bool isReadHS300 = false;
// LPS22HB
int valPressure;
bool isReadLPS = false;
// PDM -> TODO
static const char channels = 1; // default number of output channels
static const int frequency = 16000; // default PCM output frequency
short sampleBuffer[512]; // Buffer to read samples into, each sample is 16-bits
volatile int samplesRead; // Number of audio samples read

// UTILITY FUNCTIONS ===============================

void(* resetFunc) (void) = 0; // Software reset

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

void initRGBLED() {
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);    
}

bool initSensors() {
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while(1) {
      errorSequence(2);
      delay(2000);
    }
  }

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS9960 sensor!");
    while(1) {
      errorSequence(3);
      delay(2000);
    }
  } else {
    //APDS.setInterruptPin(_); // Better performance if manualy set pin
    APDS.setLEDBoost(3); //0-3
  }

  if (!HS300x.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while(1) {
      errorSequence(4);
      delay(2000);
    }
  }

  if (!BARO.begin()) {
    Serial.println("Failed to initialize pressure sensor!");
    while(1) {
      errorSequence(5);
      delay(2000);
    }
  }

  // Configure the data receive callback
  // PDM.onReceive(onPDMdata);

  // if (!PDM.begin(channels, frequency)) {
  //   Serial.println("Failed to start PDM!");
  //   while (1);
  // }
  
  return true;
}
// END OF UTILITY FUNCTIONS ===============================

void setup() {
  Serial.begin(9600);  
  initRGBLED();
  
  inLedGreen(HIGH);
  while (!Serial); // Wait for serial
  inLedGreen(LOW);
  delay(1000);

  inLedGreen(HIGH);
  while (!initSensors());
  inLedGreen(LOW);
  delay(2000);
  
  inLedBlue(HIGH);
  if (!BLE.begin()) { // Try enabling BLE
    inLedBlue(LOW);
    Serial.println("starting Bluetooth® Low Energy module failed!");
    Serial.println("Restarting...");
    errorSequence();
    resetFunc(); // Reset if not succeded
  }
  inLedBlue(LOW);
  delay(500);  

  inLedBlue(HIGH);
  BLE.setLocalName("GOLEM_Vaina");  // Set name for connection
  BLE.setAdvertisedService(customService); // add the custom service UUID
  
  customService.addCharacteristic(adpLuxChar); // add the custom characteristic UUID
  BLE.advertise();  // Start advertising
  
  Serial.print("MAC: ");
  Serial.println(BLE.address());
  Serial.println("Waiting for connections...");
  inLedBlue(LOW);
  delay(2000);
    
  readySequence(8);
}

void loop() {
  waitForConnection();
// connectToPeripheral();

  if( (millis() - mainTimer) > 1000 ){
    if(isConnected){
      readSensors();
      publishValues();
    }

    mainTimer = millis();
  }
  
  delay(100);
}

void waitForConnection() {
  BLEDevice central = BLE.central();
  if(BLE.connected()) {
    isConnected = true;  
  } else {
    isConnected = false;    
  }

  if (!isConnected && (millis() - disconnectedTimer) > 1000) {
    waitBleLed = !waitBleLed;
    if (waitBleLed){
      inLedBlue(HIGH);
    } else {
      inLedBlue(LOW);      
    }
    Serial.println("...");
    disconnectedTimer = millis();
    
  } else if (isConnected && waitBleLed) {
    waitBleLed = false;
    inLedBlue(LOW);
  }
}

void readSensors() {
  //IMU  
  if(IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(valMagnetX, valMagnetY, valMagnetZ);
  }
  //APDS
  if (APDS.colorAvailable()) {
    APDS.readColor(valColorR, valColorG, valColorB);
    valLight = (int)((valColorR + valColorG + valColorB) / 3);
  }
  if (APDS.proximityAvailable()) {
    valProximity = APDS.readProximity();
  }
  //HS300
  valTemperature = HS300x.readTemperature();
  valHumidity = HS300x.readHumidity();
  //LPS
  valPressure = BARO.readPressure();

  // if (samplesRead) {
  //   // Print samples to the serial monitor or plotter
  //   for (int i = 0; i < samplesRead; i++) {
  //     if(channels == 2) {
  //       Serial.print("L:");
  //       Serial.print(sampleBuffer[i]);
  //       Serial.print(" R:");
  //       i++;
  //     }
  //     Serial.println(sampleBuffer[i]);
  //   }
  //   // Clear the read count
  //   samplesRead = 0;
  // }  
}

void publishValues() {
  adpLuxChar.writeValue(valLight);
}
