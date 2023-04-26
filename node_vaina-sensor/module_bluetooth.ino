void setupBLE() {
  // set Names and service UUID
  String deviceName = "GOLEM_Vaina_" + BLE.address().substring(9); //last 3 bytes of the MAC address
  BLE.setDeviceName( deviceName.c_str() );
  BLE.setLocalName( deviceName.c_str() );
  BLE.setAdvertisedService( customService );
  // add Custom Characteristics
  customService.addCharacteristic(mbMagChar);
  customService.addCharacteristic(mbAccelChar);
  customService.addCharacteristic(mbGyroChar);
  customService.addCharacteristic(apdLightChar);
  customService.addCharacteristic(apdGestureChar);
  customService.addCharacteristic(adpProxChar);
  customService.addCharacteristic(hs3TempChar);
  customService.addCharacteristic(hs3HumChar);
  customService.addCharacteristic(lpsPressChar);
  customService.addCharacteristic(impulseResponseChar);
  // add Service
  BLE.addService( customService );
  
  // set BLE event handlers
  BLE.setEventHandler( BLEConnected, blePeripheralConnectHandler );
  BLE.setEventHandler( BLEDisconnected, blePeripheralDisconnectHandler );
  // start advertising
  BLE.advertise(); 

  // status prints
  Serial.print("MAC: ");
  Serial.println(String(BLE.address()));
  Serial.println("Waiting for connections...");
}

void handleBLE() {
  BLEDevice central = BLE.central();
  
  if (BLE.connected()) {

    onConnected();

  } else {

    if ( (millis() - disconnectedTimer) > UNCONNECTED_BLINK_FREQ ) {
      waitForConnection();
    }

  }
}

void waitForConnection() {
  waitBleLed = !waitBleLed;
  inLedBlue(waitBleLed);     
  //Serial.println("...");
  disconnectedTimer = millis();
}

void onConnected() {
    if( (millis() - mainTimer) > FREQ_BROADCAST ){
      if (sensorsUpdated || IRupdated){
        publishValues();
        sensorsUpdated = false;
        mainTimer = millis();
      }
    }
}


// ==================


void blePeripheralConnectHandler( BLEDevice central ) {
  waitBleLed = true;
  inLedBlue(waitBleLed);
  Serial.print("Connected to: ");
  Serial.println(String(central.address()));
}

void blePeripheralDisconnectHandler( BLEDevice central ) {
  waitBleLed = false;
  inLedBlue(waitBleLed);
  Serial.print("Disconnected from: ");
  Serial.println(String(central.address()));
}

void publishValues() {
  // https://docs.arduino.cc/tutorials/nano-33-ble-sense/cheat-sheet
  // Serial.println("Start publishing ...");

  // Magnet
  magnetValuesStr = "";
  for(int i = 0; i < 3; i++) {
    magnetValuesStr += String(magnetValues[i], 3);
    if(i < 2) {
      magnetValuesStr += ",";
    }
  }
  stringValue = String(VAINA_ID);
  stringValue += String(10);
  stringValue += magnetValuesStr; // float[3][-400,400]uT
  stringValue.getBytes( magnetBytes, sizeof(magnetBytes) );
  mbMagChar.writeValue( magnetBytes, sizeof(magnetBytes) );

  // Accel
  accelValuesStr = "";
  for(int i = 0; i < 3; i++) {
    accelValuesStr += String(accelValues[i], 3);
    if(i < 2) {
      accelValuesStr += ",";
    }
  }
  stringValue = String(VAINA_ID);
  stringValue += String(10);
  stringValue += accelValuesStr; // float[3][-4, +4]g
  stringValue.getBytes( accelBytes, sizeof(accelBytes) );
  mbAccelChar.writeValue( accelBytes, sizeof(accelBytes) );

  // Gyro
  gyroValuesStr = "";
  for(int i = 0; i < 3; i++) {
    gyroValuesStr += String(gyroValues[i], 3);
    if(i < 2) {
      gyroValuesStr += ",";
    }
  }
  stringValue = String(VAINA_ID);
  stringValue += String(10);
  stringValue += gyroValuesStr; // float[3][-2000, +2000]dps
  stringValue.getBytes( gyroBytes, sizeof(gyroBytes) );
  mbGyroChar.writeValue( gyroBytes, sizeof(gyroBytes) );

  // Color & Light
  lightValuesStr = "";
  for(int i = 0; i < 4; i++) {
    lightValuesStr += String(lightValues[i]);
    if(i < 3) {
      lightValuesStr += ",";
    }
  }
  stringValue = String(VAINA_ID);
  stringValue += String(20);
  stringValue += lightValuesStr; // int[4][0-255]
  stringValue.getBytes( lightBytes, sizeof(lightBytes) );
  apdLightChar.writeValue( lightBytes, sizeof(lightBytes) );

  // Gesture
  stringValue = String(VAINA_ID);
  stringValue += String(40);
  stringValue += valGesture; // int[0-3]
  stringValue.getBytes( gestBytes, sizeof(gestBytes) );
  apdGestureChar.writeValue( gestBytes, sizeof(gestBytes) );
  
  // Proximity
  stringValue = String(VAINA_ID);
  stringValue += String(40);
  stringValue += valProximity; // int[0-255]
  stringValue.getBytes( proxBytes, sizeof(proxBytes) );
  adpProxChar.writeValue( proxBytes, sizeof(proxBytes) );

  // Temperature
  stringValue = String(VAINA_ID);
  stringValue += String(50);
  stringValue += valTemperature; // float[-40,120]ºC
  stringValue.getBytes( tempBytes, sizeof(tempBytes) );
  hs3TempChar.writeValue( tempBytes, sizeof(tempBytes) ); 
  
  // Humidity
  stringValue = String(VAINA_ID);
  stringValue += String(60);
  stringValue += valHumidity; // float [0-100]%
  stringValue.getBytes( humBytes, sizeof(humBytes) );
  hs3HumChar.writeValue( humBytes, sizeof(humBytes) );
  
  //Presure
  stringValue = String(VAINA_ID);
  stringValue += String(70);
  stringValue += valPressure; // ???
  stringValue.getBytes( pressBytes, sizeof(pressBytes) );
  lpsPressChar.writeValue( pressBytes, sizeof(pressBytes) );

  // IR
  irValuesStr = "";
  for(int i = 0; i < FREQUENCY_BANDS; i++) {
    irValuesStr += String(resultsFFT[i], 2);
    if(i < FREQUENCY_BANDS - 1) {
      irValuesStr += ",";
    }
  }
  stringValue = String(VAINA_ID);
  stringValue += String(80);
  stringValue += irValuesStr; // ???
  stringValue.getBytes( irBytes, sizeof(irBytes) );
  impulseResponseChar.writeValue(irBytes, sizeof(irBytes));

  justNotified = NOTIFICATION_BADGE_DECAY;
  //printValuesToSerial();
  // Serial.println("... end publishing.");
}