bool setupSensors() {

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
  
  return true;
}

void handleSensors() {
  // Read sensors and raise a flag when got new values
  readSensors();
  sensorsUpdated = true;
}

void readSensors() {
  //IMU  
  if(IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(magnetValues[0], magnetValues[1], magnetValues[2]);
    magnetUpdate = true;
  }
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accelValues[0], accelValues[1], accelValues[2]);
    accelUpdate = true;
  }
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gyroValues[0], gyroValues[1], gyroValues[2]);
    gyroUpdate = true;
  }

  //APDS
  if ((APDS.colorAvailable()) && (lightUpdate == false)) {
    APDS.readColor(lightValues[0], lightValues[1], lightValues[2]);
    lightValues[4] = (int)((lightValues[0]+lightValues[1]+lightValues[2]) * 0.33);

    // lightValuesStr = "";
    // for(int i = 0; i < sizeof(lightValues); i++) {
    //   lightValuesStr += String(lightValues[i]);
    //   if(i < (sizeof(lightValues)-1)) {
    //     lightValuesStr += ",";
    //   }
    // }

    // Serial.print("LIGHT value: ");
    // Serial.println(lightValuesStr);
    lightUpdate = true;
  }
  if (APDS.gestureAvailable()) {
    valGesture = APDS.readGesture();
    gestUpdate = true;
  }
  if (APDS.proximityAvailable()) {
    valProximity = APDS.readProximity();
    proxUpdate = true;
  }

  //HS300
  valTemperature = HS300x.readTemperature();
  tempUpdate = true;

  valHumidity = HS300x.readHumidity();
  humUpdate = true;

  //LPS
  valPressure = BARO.readPressure();
  pressUpdate = true;
}

void printValuesToSerial() {
  Serial.print( "Magnet Field: " );
  Serial.print( String(magnetValues[0], 2) );
  Serial.print( " , " );
  Serial.print( String(magnetValues[1], 2) );
  Serial.print( " , " );
  Serial.println( String(magnetValues[2], 2) );
  Serial.print( "Accelerometer: " );
  Serial.print( String(accelValues[0], 2) );
  Serial.print( " , " );
  Serial.print( String(accelValues[1], 2) );
  Serial.print( " , " );
  Serial.println( String(accelValues[2], 2) );
  Serial.print( "Gyroscope: " );
  Serial.print( String(gyroValues[0], 2) );
  Serial.print( " , " );
  Serial.print( String(gyroValues[1], 2) );
  Serial.print( " , " );
  Serial.println( String(gyroValues[2], 2) );
  Serial.print( "Color: " );
  Serial.print( String(lightValues[0]) );
  Serial.print( " , " );
  Serial.print( String(lightValues[1]) );
  Serial.print( " , " );
  Serial.println( String(lightValues[2]) );
  Serial.print( "Light: " );
  Serial.println( String(lightValues[4]) );
  Serial.print( "Gesture: " );
  Serial.println( String(valGesture) );
  Serial.print( "Proximity: " );
  Serial.println( String(valProximity) );
  Serial.print( "Temperature: " );
  Serial.println( String(valTemperature, 2) );
  Serial.print( "Humidity: " );
  Serial.println( String(valHumidity, 2) );
  Serial.print( "Pressure: " );
  Serial.println( String(valPressure, 2) );
}