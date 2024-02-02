void handleSerial() {
  if( (millis() - mainTimer) > FREQ_BROADCAST ){
      // Serial.println("onConnected: FLAG 1");
      if (sensorsUpdated || IRupdated){
        // Serial.println("onConnected: FLAG 2");
        publishValuesSerial();
        // Serial.println("onConnected: FLAG 3");
        sensorsUpdated = false;
        mainTimer = millis();
      }
    } 
}

void publishValuesSerial() {
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
        
    stringValue += "$";
    stringValue += String(10);
    stringValue += magnetValuesStr; // float[3][-400,400]uT
    stringValue += "\n";
    
    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);

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

    stringValue += "$";
    stringValue += String(11);
    stringValue += accelValuesStr; // float[3][-4, +4]g
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);
    
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

    stringValue += "$";
    stringValue += String(12);
    stringValue += gyroValuesStr; // float[3][-2000, +2000]dps
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );  
    // delay(200);
    
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

    stringValue += "$";
    stringValue += String(20);
    stringValue += lightValuesStr; // int[4][0-255]
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);
    
    lightUpdate = false;
  }

  // Serial.println("publishValues: FLAG 4");
  // Gesture
  if (gestUpdate) {
    // stringValue += "$";
    // stringValue += String(40);
    // stringValue += valGesture; // int[0-3]
    // stringValue += "\n";

    // byte plain[stringValue.length()];
    // stringValue.getBytes(plain, stringValue.length() );
    // Serial.write( plain, stringValue.length() );
    // delay(200);
    
    gestUpdate = false;
  }
  
  // Serial.println("publishValues: FLAG 5");
  // Proximity
  if (proxUpdate) {
    stringValue += "$";
    stringValue += String(40);
    stringValue += valProximity; // int[0-255]
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);
    
    proxUpdate = false;
  }

  // Serial.println("publishValues: FLAG 6");
  // Temperature
  if (tempUpdate) {
    stringValue += "$";
    stringValue += String(50);
    stringValue += valTemperature; // float[-40,120]ºC
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() ); 
    // delay(200);
    
    tempUpdate = false;
  }
  
  // Serial.println("publishValues: FLAG 7");
  // Humidity
  if (humUpdate) {
    stringValue += "$";
    stringValue += String(60);
    stringValue += valHumidity; // float [0-100]%
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);
    
    humUpdate = false;
  }
  
  // Serial.println("publishValues: FLAG 8");
  //Presure
  if (pressUpdate) {
    stringValue += "$";
    stringValue += String(70);
    stringValue += valPressure; // ???
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);
    
    pressUpdate = false;
  }

  // Serial.println("publishValues: FLAG 9");
  // IR
  if (IRupdated) {
    irValuesStr = "";
    for(int i = 0; i < FREQUENCY_BANDS; i++) {
      irValuesStr += String(resultsFFT[i], 2);
      if(i < FREQUENCY_BANDS - 1) {
        irValuesStr += ",";
      }
    }

    stringValue += "$";
    stringValue += String(80);
    stringValue += irValuesStr; // ???
    stringValue += "\n";

    byte plain[stringValue.length()];
    stringValue.getBytes(plain, stringValue.length() );
    Serial.write( plain, stringValue.length() );
    // delay(200);

    IRupdated = false;
  }

  justNotified = NOTIFICATION_BADGE_DECAY;
  //printValuesToSerial();
  // Serial.println("... end publishing.");
}