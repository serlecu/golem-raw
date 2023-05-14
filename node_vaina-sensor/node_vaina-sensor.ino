#include <Arduino_BMI270_BMM150.h> // Inertial Measurement Unit
#include <Arduino_APDS9960.h> // Digital proximity and ambient light as well as for detecting RGB colors and gestures.
#include <Arduino_HS300x.h> // Temperature and humidty
#include <Arduino_LPS22HB.h> // Barometric pressure

#include <PDM.h> // Pulse-density modulation microphones
#include <arduinoFFT.h>
// Check: #include <ArduinoSound.h> // bugs in BLE 33 Sense

#include <ArduinoBLE.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// #include <Thread.h>
#include <mbed.h>
using namespace mbed;
#include <rtos.h>
#include <platform.h>
// #include <Arduino_Threads.h>

// ====== PRIMITIVE FUNCTS =======

// Utilities
void(* resetFunc) (void) = 0; // Software reset
void inLedRed(bool);
void inLedGreen(bool);
void inLedBlue(bool);
void readySequence(int);
void errorSequence(int);
// Setup
void setupRGBLED();
void setupOLED(void);
bool setupSensors(void);
bool setupIR(void);
bool createImpulse(void);
void setupBLE(void);
// Handlers
void handleBLE(void);
void handleIR(void);
void handleSensors(void);
void handleOLED(void);
void handleSerial(void);

// ====== VARAIBLES ======

// -- Main -- //
#define SERIAL_MODE false
#define VAINA_ID 0 // DONT REMEMBER IF USED ON CLIENT
#define UNCONNECTED_BLINK_FREQ 1000
#define FREQ_BROADCAST 1000
bool isConnected = false; //miss
bool waitBleLed = false; //Blue Blink while waiting for connection
unsigned long disconnectedTimer;
unsigned long mainTimer;
Ticker tickerBlink; 
DigitalOut led1(LED1); // test against freeze

// -- Sensors -- //
bool sensorsUpdated = false;
// update flags
bool magnetUpdate = false;
bool accelUpdate = false;
bool gyroUpdate = false;
bool lightUpdate = false;
bool gestUpdate = false;
bool proxUpdate = false;
bool tempUpdate = false;
bool humUpdate = false;
bool pressUpdate = false;
bool irUpdate = false;
// Sensors - BMI270 & BMM150
float magnetValues[3];
float accelValues[3]; //miss
float gyroValues[3]; //miss
// Sensors - APD
int lightValues[3];
int valGesture;
int valProximity;
// Sensors - HS300x
float valTemperature, valHumidity;
bool isReadHS300 = false; //miss
// Sensors - LPS22HB
float valPressure;
bool isReadLPS = false; //miss

// -- Audio -- //
#define AUDIO_IMPULSE_FREQ 10000
unsigned long IRtimer = 0;
volatile bool isIRon = false;
volatile bool isPlaying = false;
volatile bool canPlay = false; // needed when threaded
volatile bool wasPlaying = false; // not needed if Threaded
volatile bool isRecording = false;
volatile bool wasRecording = false;
volatile bool doProcessProfile = false;
volatile int isIRprocessing = 0;
bool IRupdated = false;
// Impulse
#include "noise_sample.h"
#define IBUFFER_SIZE 2048 //512
#define IBUFFER_MILLIS 1000
rtos::Thread impulseThread;
Ticker audioTicker;
PwmOut PWM_A( digitalPinToPinName( 2 ) );
volatile int playingSample = 0;
volatile bool endSample = false;
// Record: PDM
static const char channels = 1; // default number of output channels
static const int frequency = 16000; // default PCM output frequency
#define MAX_REC_SAMPLES 1024
short tempBuffer[128];
volatile int freshSamples = 0;
int readingSample = 0;
// Profile
#define SAMPLES 1024 // power of 2
#define SAMPLING_FREQ 24000 // 12 kHz Fmax = sampleF /2 
#define AMPLITUDE 100 // sensitivity
#define FREQUENCY_BANDS 8
double vImag[SAMPLES];
double vReal[SAMPLES];
arduinoFFT fft = arduinoFFT(vReal, vImag, SAMPLES, SAMPLING_FREQ);
float reference = log10(50.0); // adjust reference to get removed background noise noise
double coutoffFrequencies[FREQUENCY_BANDS];
volatile double resultsFFT[FREQUENCY_BANDS];

// -- Bluetooth LE -- //
BLEDevice central;
bool wasConnected = false;
uint8_t magnetBytes[512], accelBytes[512], gyroBytes[512];
uint8_t lightBytes[512], gestBytes[512], proxBytes[512];
uint8_t tempBytes[512], humBytes[512], pressBytes[512];
uint8_t irBytes[512];
String stringValue, magnetValuesStr, accelValuesStr, gyroValuesStr, lightValuesStr, irValuesStr;
// Service
BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // create a custom service
// Characteristics
BLECharacteristic mbMagChar("19B10010-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
BLECharacteristic mbAccelChar("19B10011-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic mbGyroChar("19B10012-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic apdLightChar("19B10020-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic apdGestureChar("19B10030-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic adpProxChar("19B10040-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic hs3TempChar("19B10050-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic hs3HumChar("19B10060-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic lpsPressChar("19B10070-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic impulseResponseChar("19B10080-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);

// -- OLED -- //
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define NOTIFICATION_BADGE_DECAY 3
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
int justNotified = 0;
int launchIR = 0;
bool isMacScrolling = false;
int displayErrorOLED = 0;



// ====== SETUP ============

void setup() {
  setupRGBLED();
  tickerBlink.attach(&blink, 1);

  // --- OLED ---
  inLedGreen(HIGH);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    errorSequence(1);
  }
  setupOLED();
  inLedGreen(LOW);
  delay(1500);

  // --- SERIAL ---
  inLedGreen(HIGH);
  Serial.begin(115200);
  delay(1500);
  while (!Serial && SERIAL_MODE);
  if (!Serial){
    errorSequence(2);
  }
  inLedGreen(LOW);
  delay(1500);
  
  // --- SENSORS ---
  inLedGreen(HIGH);
  while (!setupSensors());
  inLedGreen(LOW);
  delay(1500);

  // --- AUDIO ---
  inLedGreen(HIGH);
  // Initialize PDM and IR
  if(!setupIR()){
    Serial.println( "starting IR failed!" );
    // Serial.println( "Restarting..." );
    errorSequence(3);
    // resetFunc(); // Reset if not succeded
  }
  inLedGreen(LOW);
  delay(1500);
  
  // --- BLE ---
  inLedBlue(HIGH);
  if (!BLE.begin()) { // Try enabling BLE
    inLedBlue(LOW);
    Serial.println( "starting Bluetooth® Low Energy module failed!" );
    Serial.println( "Restarting..." );
    errorSequence(4);
    resetFunc(); // Reset if not succeded
  }
  inLedBlue(LOW);
  delay(500);  

  inLedBlue(HIGH);
  setupBLE();
  inLedBlue(LOW);
  delay(1500);

  // All OK  
  readySequence(4);
}


// ====== MAIN LOOP =============

void loop() {

  // handleBLE();
  handleIR(true);//wasConnected);
  handleSensors();
  handleSerial();
  handleOLED();

  delay(1);
}
