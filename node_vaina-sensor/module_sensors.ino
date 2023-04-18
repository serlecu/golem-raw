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


void handleSensors() {
  // Read sensors and raise a flag when got new values
  readSensors();
  sensorsUpdated = true;
}


  // Configure the data receive callback
  // PDM.onReceive(onPDMdata);

  // if (!PDM.begin(channels, frequency)) {
  //   Serial.println("Failed to start PDM!");
  //   while (1);
  // }
  
  return true;
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

void printValuesToSerial() {
  Serial.print( "Magnet Field: " );
  Serial.print( String(valMagnetX, 2) );
  Serial.print( " , " );
  Serial.print( String(valMagnetY, 2) );
  Serial.print( " , " );
  Serial.println( String(valMagnetZ, 2) );
  Serial.print( "Color: " );
  Serial.print( String(valColorR) );
  Serial.print( " , " );
  Serial.print( String(valColorG) );
  Serial.print( " , " );
  Serial.println( String(valColorB) );
  Serial.print( "Light: " );
  Serial.println( String(valLight) );
  Serial.print( "Proximity: " );
  Serial.println( String(valProximity) );
  Serial.print( "Temperature: " );
  Serial.println( String(valTemperature, 2) );
  Serial.print( "Humidity: " );
  Serial.println( String(valHumidity, 2) );
  Serial.print( "Pressure: " );
  Serial.println( String(valPressure, 2) );
  // impulseResponseChar.writeValue(-1);
}