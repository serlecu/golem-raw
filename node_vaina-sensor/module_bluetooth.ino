void setupBLE() {
  // set Names and service UUID
  String deviceName = "GOLEM_Vaina_" + BLE.address().substring(9); //last 3 bytes of the MAC address
  BLE.setDeviceName( deviceName.c_str() );
  BLE.setLocalName( deviceName.c_str() );
  BLE.setConnectable(true);
  // BLE.setAdvertisingInterval(30); // 48 * 0.625
  // BLE.setConnectionInterval(5, 10); // 7.5 ms minimum, 4 s maximum (* 1,25 )

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

  firstPublish();
  
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
  if (!central) {
    // Serial.println("handleBLE: FLAG 0");
    central = BLE.central();
  }

  if (!BLE.connected()){

    if( wasConnected ){
      // delay(10);
      wasConnected = false;
    }
      waitForConnection();


  } else {
      // Serial.println("handleBLE: FLAG 1");
    if( !wasConnected ){
      // Serial.println("handleBLE: FLAG 2");
      // central = BLE.central();
      wasConnected = true;
      // Serial.println("handleBLE: FLAG 3");
    }

    if (central.connected()){
      // Serial.println("handleBLE: FLAG 4");
    }
    onConnected();
  }
  
}

void waitForConnection() {
  if ( (millis() - disconnectedTimer) > UNCONNECTED_BLINK_FREQ ) {
    waitBleLed = !waitBleLed;
    inLedBlue(waitBleLed);     
    //Serial.println("...");
    disconnectedTimer = millis();
  }
}

void onConnected() {
  // Serial.println("onConnected: FLAG 0");
    if( (millis() - mainTimer) > FREQ_BROADCAST ){
      // Serial.println("onConnected: FLAG 1");
      if (sensorsUpdated || IRupdated){
        // Serial.println("onConnected: FLAG 2");
        publishValues();
        // Serial.println("onConnected: FLAG 3");
        sensorsUpdated = false;
        mainTimer = millis();
      }
    }
  // Serial.println("onConnected: FLAG 4");
}


// ==================


void blePeripheralConnectHandler( BLEDevice central ) {
  // Serial.println("blePeripheralConnectHandler: FLAG 0");
  waitBleLed = true;
  inLedBlue(waitBleLed);
  Serial.print("Connected to: ");
  Serial.println(String(central.address()));
  central = BLE.central();
  // Serial.println("blePeripheralConnectHandler: FLAG 1");
  // delay(1);
}

void blePeripheralDisconnectHandler( BLEDevice central ) {
  // Serial.println("blePeripheralDisonnectHandler: FLAG 0");
  waitBleLed = false;
  inLedBlue(waitBleLed);
  Serial.print("Disconnected from: ");
  Serial.println(String(central.address()));
  central = BLE.central();
  // Serial.println("blePeripheralDisonnectHandler: FLAG 1");
}

void firstPublish() {
  stringValue = String(VAINA_ID);
  stringValue += String(10);
  stringValue.getBytes( magnetBytes, sizeof(magnetBytes) );
  mbMagChar.writeValue( magnetBytes, sizeof(magnetBytes) );
  magnetUpdate = false;

  // Accel
  stringValue = String(VAINA_ID);
  stringValue += String(10);
  stringValue.getBytes( accelBytes, sizeof(accelBytes) );
  mbAccelChar.writeValue( accelBytes, sizeof(accelBytes) );
  accelUpdate = false;

  // Gyro
  stringValue = String(VAINA_ID);
  stringValue += String(10);
  stringValue.getBytes( gyroBytes, sizeof(gyroBytes) );
  mbGyroChar.writeValue( gyroBytes, sizeof(gyroBytes) );
  gyroUpdate = false;

  // Color & Light
  stringValue = String(VAINA_ID);
  stringValue += String(20);
  stringValue.getBytes( lightBytes, sizeof(lightBytes) );
  apdLightChar.writeValue( lightBytes, sizeof(lightBytes) );
  lightUpdate = false;

  // Gesture
  stringValue = String(VAINA_ID);
  stringValue += String(40);
  stringValue.getBytes( gestBytes, sizeof(gestBytes) );
  apdGestureChar.writeValue( gestBytes, sizeof(gestBytes) );
  gestUpdate = false;
  
  // Proximity
  stringValue = String(VAINA_ID);
  stringValue += String(40);
  stringValue.getBytes( proxBytes, sizeof(proxBytes) );
  adpProxChar.writeValue( proxBytes, sizeof(proxBytes) );
  proxUpdate = false;

  // Temperature
  stringValue = String(VAINA_ID);
  stringValue += String(50);
  stringValue.getBytes( tempBytes, sizeof(tempBytes) );
  hs3TempChar.writeValue( tempBytes, sizeof(tempBytes) ); 
  tempUpdate = false;
  
  // Humidity
  stringValue = String(VAINA_ID);
  stringValue += String(60);
  stringValue.getBytes( humBytes, sizeof(humBytes) );
  hs3HumChar.writeValue( humBytes, sizeof(humBytes) );
  humUpdate = false;
  
  //Presure
  stringValue = String(VAINA_ID);
  stringValue += String(70);
  stringValue.getBytes( pressBytes, sizeof(pressBytes) );
  lpsPressChar.writeValue( pressBytes, sizeof(pressBytes) );
  pressUpdate = false;

  // IR
  stringValue = String(VAINA_ID);
  stringValue += String(80);
  stringValue.getBytes( irBytes, sizeof(irBytes) );
  impulseResponseChar.writeValue(irBytes, sizeof(irBytes));
  irUpdate = false;
}

void publishValues() {
  // https://docs.arduino.cc/tutorials/nano-33-ble-sense/cheat-sheet
  // Serial.println("Start publishing ...");
  // Serial.println("publishValues: FLAG 0");
  // Magnet
  if (magnetUpdate) {
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

    magnetUpdate = false;
  }

  // Serial.println("publishValues: FLAG 1");
  // Accel
  if (accelUpdate) {
    accelValuesStr = "";
    for(int i = 0; i < 3; i++) {
      accelValuesStr += String(accelValues[i], 3);
      if(i < 2) {
        accelValuesStr += ",";
      }
    }
    stringValue = String(VAINA_ID);
    stringValue += String(11);
    stringValue += accelValuesStr; // float[3][-4, +4]g
    stringValue.getBytes( accelBytes, sizeof(accelBytes) );
    mbAccelChar.writeValue( accelBytes, sizeof(accelBytes) );

    accelUpdate = false;
  }

  // Serial.println("publishValues: FLAG 2");
  // Gyro
  if (gyroUpdate) {    
    gyroValuesStr = "";
    for(int i = 0; i < 3; i++) {
      gyroValuesStr += String(gyroValues[i], 3);
      if(i < 2) {
        gyroValuesStr += ",";
      }
    }
    stringValue = String(VAINA_ID);
    stringValue += String(12);
    stringValue += gyroValuesStr; // float[3][-2000, +2000]dps
    stringValue.getBytes( gyroBytes, sizeof(gyroBytes) );
    mbGyroChar.writeValue( gyroBytes, sizeof(gyroBytes) );

    gyroUpdate = false;
  }

  // Serial.println("publishValues: FLAG 3");
  // Color & Light
  if (lightUpdate) {
    lightValuesStr = "";
    for(int i = 0; i < 3; i++) {
      lightValuesStr += String(lightValues[i]);
      if(i < 2) {
        lightValuesStr += ",";
      }
    }
    // Serial.println(lightValuesStr);
    stringValue = String(VAINA_ID);
    stringValue += String(20);
    stringValue += lightValuesStr; // int[4][0-255]
    stringValue.getBytes( lightBytes, sizeof(lightBytes) );
    apdLightChar.writeValue( lightBytes, sizeof(lightBytes) );

    lightUpdate = false;
  }

  // Serial.println("publishValues: FLAG 4");
  // Gesture
  if (gestUpdate) {
    stringValue = String(VAINA_ID);
    stringValue += String(40);
    stringValue += valGesture; // int[0-3]
    stringValue.getBytes( gestBytes, sizeof(gestBytes) );
    apdGestureChar.writeValue( gestBytes, sizeof(gestBytes) );

    gestUpdate = false;
  }
  
  // Serial.println("publishValues: FLAG 5");
  // Proximity
  if (proxUpdate) {
    stringValue = String(VAINA_ID);
    stringValue += String(40);
    stringValue += valProximity; // int[0-255]
    stringValue.getBytes( proxBytes, sizeof(proxBytes) );
    adpProxChar.writeValue( proxBytes, sizeof(proxBytes) );

    proxUpdate = false;
  }

  // Serial.println("publishValues: FLAG 6");
  // Temperature
  if (tempUpdate) {
    stringValue = String(VAINA_ID);
    stringValue += String(50);
    stringValue += valTemperature; // float[-40,120]ºC
    stringValue.getBytes( tempBytes, sizeof(tempBytes) );
    hs3TempChar.writeValue( tempBytes, sizeof(tempBytes) ); 

    tempUpdate = false;
  }
  
  // Serial.println("publishValues: FLAG 7");
  // Humidity
  if (humUpdate) {
    stringValue = String(VAINA_ID);
    stringValue += String(60);
    stringValue += valHumidity; // float [0-100]%
    stringValue.getBytes( humBytes, sizeof(humBytes) );
    hs3HumChar.writeValue( humBytes, sizeof(humBytes) );

    humUpdate = false;
  }
  
  // Serial.println("publishValues: FLAG 8");
  //Presure
  if (pressUpdate) {
    stringValue = String(VAINA_ID);
    stringValue += String(70);
    stringValue += valPressure; // ???
    stringValue.getBytes( pressBytes, sizeof(pressBytes) );
    lpsPressChar.writeValue( pressBytes, sizeof(pressBytes) );

    pressUpdate = false;
  }

  // Serial.println("publishValues: FLAG 9");
  // IR
  if (irUpdate) {
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
     irUpdate = false;
  }

  justNotified = NOTIFICATION_BADGE_DECAY;
  //printValuesToSerial();
  // Serial.println("... end publishing.");
}