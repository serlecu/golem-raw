void setupBLE() {
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
}

void handleBLE() {
  BLEDevice central = BLE.central();
  
  if (BLE.connected()) {
    if (!wasConnected){
      Serial.println("Connected!");
    }

    onConnected();

  } else {
    if (wasConnected){
      Serial.println("Disconnected!");
    }

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
  Serial.println(central.address());
}

void blePeripheralDisconnectHandler( BLEDevice central ) {
  waitBleLed = false;
  inLedBlue(waitBleLed);
  Serial.print("Disconnected from: ");
  Serial.println(central.address());
}

void publishValues() {
  // https://docs.arduino.cc/tutorials/nano-33-ble-sense/cheat-sheet
  Serial.println("Start publishing ...");
  // //Magnet
  stringValue = String(VAINA_ID) + String(10) + String(valMagnetX);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  BMMagXChar.writeValue( byteArray, sizeof(byteArray) ); // float[-400,400]
  // Serial.println(stringValue);
  stringValue = String(VAINA_ID) + String(11) + String(valMagnetY);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  BMMagYChar.writeValue( byteArray, sizeof(byteArray) ); // float[-400,400]
  // Serial.println(stringValue);
  stringValue = String(VAINA_ID) + String(12) + String(valMagnetZ);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  BMMagZChar.writeValue( byteArray, sizeof(byteArray) ); // float[-400,400]
  // Serial.println(stringValue);
  
  // //Lux
  stringValue = String(VAINA_ID) + String(20) + String(valLight);
  stringValue.getBytes( byteArray, sizeof(byteArray) ); // int[0-255]
  adpLuxChar.writeValue( byteArray, sizeof(byteArray) ); // float[-400,400]
  // Serial.println(stringValue);

  // // //Color
  // stringValue = String(VAINA_ID) + String(21) + String(valColorR) +","+String(valColorG)+","+String(valColorB);
  stringValue = String(VAINA_ID) + String(22) + String(valColorR);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  apdColorRChar.writeValue( byteArray, sizeof(byteArray) ); // int[0-255]
  // Serial.println(stringValue);
  stringValue = String(VAINA_ID) + String(22) + String(valColorG);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  apdColorGChar.writeValue( byteArray, sizeof(byteArray) ); // int[0-255]
  stringValue = String(VAINA_ID) + String(23) + String(valColorB);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  apdColorBChar.writeValue( byteArray, sizeof(byteArray) ); // int[0-255]
  
  // // //Proximity
  stringValue = String(VAINA_ID) + String(40) + String(valProximity);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  adpProxChar.writeValue( byteArray, sizeof(byteArray) ); // int[0-255]

  // //Temperature
  stringValue = String(VAINA_ID) + String(50) + String(valTemperature);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  hs3TempChar.writeValue( byteArray, sizeof(byteArray) ); // float[-40,120]
  
  //Humidity
  stringValue = String(VAINA_ID) + String(60) + String(valHumidity);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  hs3HumChar.writeValue( byteArray, sizeof(byteArray) );
  
  //Presure
  stringValue = String(VAINA_ID) + String(70) + String(valPressure);
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  lpsPressChar.writeValue( byteArray, sizeof(byteArray) );

  // IR
  String strArray = "";
  for(int i = 0; i < arrayLength; i++) {
    myString += String(resultsFFT[i], 2);
    if(i < arrayLength - 1) {
      myString += ",";
    }
  }
  stringValue = String(VAINA_ID) + String(80) + strArray;
  stringValue.getBytes( byteArray, sizeof(byteArray) );
  impulseResponseChar.writeValue(byteArray, sizeof(byteArray));

  justNotified = NOTIFICATION_BADGE_DECAY;
  printValuesToSerial();
  Serial.println("... end publishing.");
}