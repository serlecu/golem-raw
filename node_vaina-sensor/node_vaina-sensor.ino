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
#include <rtos.h>
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

// ====== VARAIBLES ======

// Main
#define VAINA_ID 0 // DONT REMEMBER IF USED ON CLIENT
#define UNCONNECTED_BLINK_FREQ 1000
#define FREQ_BROADCAST 250
bool isConnected = false; //miss
bool waitBleLed = false; //Blue Blink while waiting for connection
unsigned long disconnectedTimer;
unsigned long mainTimer;
// rtos::Thread impulseThread = new rtos::Thread(osPriorityRealtime, OS_STACK_SIZE);
// rtos::Thread recordingThread = new rtos::Thread(osPriorityRealtime, OS_STACK_SIZE);
rtos::Thread impulseThread;

// Sensors
bool sensorsUpdated = false;
// Sensors - BMI270 & BMM150
float valAccelX, valAccelY, valAccelZ; //miss
float valGyroX, valGyroY, valGyroZ; //miss
float valMagnetX, valMagnetY, valMagnetZ;
// Sensors - APD
int valColorR, valColorG, valColorB;
int valLight;
int valProximity;
// Sensors - HS300x
float valTemperature, valHumidity;
bool isReadHS300 = false; //miss
// Sensors - LPS22HB
float valPressure;
bool isReadLPS = false; //miss

// Audio
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
#define IBUFFER_SIZE 1024
#define PWM_PIN_A 2
#define PWM_PIN_B 3
double impulseBufferA[IBUFFER_SIZE];
double impulseBufferB[IBUFFER_SIZE];
int playingSample = 0;
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
#define FREQUENCY_BANDS 14
double vImag[SAMPLES];
double vReal[SAMPLES];
unsigned long sampling_period_us;
arduinoFFT fft = arduinoFFT(vReal, vImag, SAMPLES, SAMPLING_FREQ);
float reference = log10(50.0); // adjust reference to get removed background noise noise
double coutoffFrequencies[FREQUENCY_BANDS];
volatile double resultsFFT[FREQUENCY_BANDS];

// Bluetooth LE
bool wasConnected = false;
uint8_t byteArray[512];
String stringValue = "";
int length = 0;
// Service
BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // create a custom service
// Characteristics
BLECharacteristic BMMagXChar("19B10010-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
BLECharacteristic BMMagYChar("19B10011-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic BMMagZChar("19B10012-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic apdColorRChar("19B10020-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic apdColorGChar("19B10021-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic apdColorBChar("19B10022-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic adpLuxChar("19B10023-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic adpProxChar("19B10040-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic hs3TempChar("19B10050-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic hs3HumChar("19B10060-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic lpsPressChar("19B10070-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);
BLECharacteristic impulseResponseChar("19B10080-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512);

// OLED
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define NOTIFICATION_BADGE_DECAY 5
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
int justNotified = 0;
int launchIR = 0;
bool isMacScrolling = false;
int displayErrorOLED = 0;



// ====== SETUP ============

void setup() {
  setupRGBLED();

  // --- OLED ---
  inLedGreen(HIGH);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    errorSequence(2);
  }
  setupOLED();
  inLedGreen(LOW);
  delay(1500);

  // --- SERIAL ---
  inLedGreen(HIGH);
  Serial.begin(115200);
  inLedGreen(LOW);  
  delay(500);
  
  if (!Serial){
    errorSequence(1);
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
    errorOLED(30);
  }
  if (!createImpulse()){
    errorOLED(31);
  }
  inLedGreen(LOW);
  delay(1500);
  
  // --- BLE ---
  inLedBlue(HIGH);
  if (!BLE.begin()) { // Try enabling BLE
    inLedBlue(LOW);
    Serial.println( "starting Bluetooth® Low Energy module failed!" );
    Serial.println( "Restarting..." );
    errorSequence(3);
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

  handleBLE();
  handleIR();
  handleSensors();
  handleOLED();

  delay(10);
}
