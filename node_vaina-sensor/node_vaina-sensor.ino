#include <ArduinoBLE.h>
#include "Arduino_BMI270_BMM150.h" // Inertial Measurement Unit
#include <Arduino_APDS9960.h> // Digital proximity and ambient light as well as for detecting RGB colors and gestures.
#include <Arduino_HS300x.h> // Temperature and humidty
#include <Arduino_LPS22HB.h> // Barometric pressure
#include <PDM.h> // Pulse-density modulation microphones
// Check #include <ArduinoSound.h>
#include <Adafruit_SSD1306.h>

void(* resetFunc) (void) = 0; // Software reset
void inLedRed(bool);
void inLedGreen(bool);
void inLedBlue(bool);
void readySequence(int);
void errorSequence(int);
void initRGBLED();

bool initSensors();
void readSensors();
void printValuesToSerial();

void blePeripheralConnectHandler( BLEDevice );
void blePeripheralDisconnectHandler( BLEDevice );
void publishValues();

void handleOLED();
void scrollingMAC();


BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // create a custom service
//Magnet
BLECharacteristic BMMagXChar("19B10010-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
BLECharacteristic BMMagYChar("19B10011-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
BLECharacteristic BMMagZChar("19B10012-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//Color
BLECharacteristic apdColorRChar("19B10020-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
BLECharacteristic apdColorGChar("19B10021-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
BLECharacteristic apdColorBChar("19B10022-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//Lux
BLECharacteristic adpLuxChar("19B10023-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//Proximity
BLECharacteristic adpProxChar("19B10040-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//Temperature
BLECharacteristic hs3TempChar("19B10050-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//Humidity
BLECharacteristic hs3HumChar("19B10060-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//Presure
BLECharacteristic lpsPressChar("19B10070-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 512); // create a custom characteristic
//IR
//BLEUnsignedCharCharacteristic impulseResponseChar("19B10008-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // create a custom characteristic


// Mains
const int VAINA_ID = 0; // DONT REMEMBER IF USED ON CLIENT
const int FREQ_BROADCAST = 250;
bool isConnected = false; //miss
bool waitBleLed = false; //Blue Blink while waiting for connection
unsigned long disconnectedTimer;
unsigned long mainTimer;

// OLED
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
#define NOTIFICATION_BADGE_DECAY 10
int justNotified = 0;
bool isMacScrolling = false;

// BLE
uint8_t byteArray[512];
String stringValue = "";
int length = 0;

// BMI270 & BMM150
float valAccelX, valAccelY, valAccelZ; //miss
float valGyroX, valGyroY, valGyroZ; //miss
float valMagnetX, valMagnetY, valMagnetZ;
// APD
int valColorR, valColorG, valColorB;
int valLight;
int valProximity;
// HS300x
float valTemperature, valHumidity;
bool isReadHS300 = false; //miss
// LPS22HB
float valPressure;
bool isReadLPS = false; //miss
// PDM -> TODO
static const char channels = 1; // default number of output channels
static const int frequency = 16000; // default PCM output frequency
short sampleBuffer[512]; // Buffer to read samples into, each sample is 16-bits
volatile int samplesRead; // Number of audio samples read



// ====== SETUP ============

void setup() {
  Serial.begin(9600);  
  initRGBLED();
  delay(1000);
  
  inLedGreen(HIGH);
  if (!Serial){
    errorSequence(1);
  } // Wait for serial
  inLedGreen(LOW);
  delay(1000);

  inLedGreen(HIGH);
  while (!initSensors());
  inLedGreen(LOW);
  delay(1000);

  inLedGreen(HIGH);
  // Initialize OLED display
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    errorSequence(2);
  }
  inLedGreen(LOW);
  delay(2000);
  
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
  // set Names and service UUID
  String deviceName = "GOLEM_Vaina_" + BLE.address().substring(9); //last 3 bytes of the MAC address
  BLE.setDeviceName( deviceName.c_str() );
  BLE.setLocalName( deviceName.c_str() );
  BLE.setAdvertisedService( customService );
  // add Custom Characteristics
  customService.addCharacteristic(BMMagXChar);
  customService.addCharacteristic(BMMagYChar);
  customService.addCharacteristic(BMMagZChar);
  customService.addCharacteristic(apdColorRChar);
  customService.addCharacteristic(apdColorGChar);
  customService.addCharacteristic(apdColorBChar);
  customService.addCharacteristic(adpLuxChar);
  customService.addCharacteristic(adpProxChar);
  customService.addCharacteristic(hs3TempChar);
  customService.addCharacteristic(hs3HumChar);
  customService.addCharacteristic(lpsPressChar);
  // customService.addCharacteristic(impulseResponseChar);
  // add Service
  BLE.addService( customService );
  
  // set BLE event handlers
  BLE.setEventHandler( BLEConnected, blePeripheralConnectHandler );
  BLE.setEventHandler( BLEDisconnected, blePeripheralDisconnectHandler );
  // start advertising
  BLE.advertise(); 

  // status prints
  Serial.print("MAC: ");
  Serial.println(BLE.address());
  Serial.println("Waiting for connections...");
  inLedBlue(LOW);
  delay(2000);
    
  readySequence(8);
}

void loop() {
  BLEDevice central = BLE.central();
  
  if (!BLE.connected() && (millis() - disconnectedTimer) > 1000) {
    waitForConnection();
  
  } else if ( BLE.connected() ) {
    handleConnection(); 
  }
  
  handleOLED();

  delay(20);
}

void waitForConnection() {
  waitBleLed = !waitBleLed;
  inLedBlue(waitBleLed);     
  //Serial.println("...");
  disconnectedTimer = millis();

  // Only for debug
  justNotified = NOTIFICATION_BADGE_DECAY;
}

void handleConnection() {
  while ( BLE.connected() ) {
    if( (millis() - mainTimer) > FREQ_BROADCAST ){
      readSensors();
      publishValues();
    
      mainTimer = millis();
    }
    delay(50);
  }
}
