void setupIR() {
  pinMode(2, OUTPUT);
  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }

  sampling_period_us = (1.0 / SAMPLING_FREQ ) * pow(10.0, 6);

  // Calculate cuttoff frequencies,meake a logarithmic scale base basePOt
  double basePot = pow(SAMPLING_FREQ / 2.0, 1.0 / FREQUENCY_BANDS);
  coutoffFrequencies[0] = basePot;
  for (int i = 1 ; i < FREQUENCY_BANDS; i++ ) {
    coutoffFrequencies[i] = basePot * coutoffFrequencies[i - 1];
  }
}

void handleIR() {

  if ( (millis() - IRtimer) > AUDIO_IMPULSE_FREQ ) {
    justNotified = NOTIFICATION_BADGE_DECAY; // bang in OLED
    isIRon = true; // flag for start IR routine
    isPlaying = true;
    isRecording = true;
    IRtimer = millis();
  }

  if ( isIRon ) {
    playImpulseParallel();
    takeSamplesPDM();
    //processIRProfile();
  }

}



void createImpulse() {
  for (int i = 0; i < IBUFFER_SIZE; i++) {
    // Generate random noise data between -32768 and 32767
    //impulseBuffer[i] = doube(random(-32768, 32767));
    //impulseBuffer[i] = (int16_t)map(i,-32768, 32767,100,255) ;
    impulseBuffer[i] = (double)map(i,0,IBUFFER_SIZE, -32768, 32767) ;
  }
}

void playImpulse() {
  Serial.println("Start Impulse ...");
  // Play noise from buffer A
  for (int i = 0; i < IBUFFER_SIZE; i++) {
    analogWrite(2, impulseBuffer[i] / 16 + 2048); // Output audio data as PWM signal to pin A0
    delayMicroseconds(sampling_period_us);// 62.5); // Wait for 1/16000s (62.5us) for 16000Hz sample rate
  }
  Serial.println("... end Impulse.");
}

void playImpulseParallel() {
  
  if (isPlaying) {
    if(!wasPlaying){
      Serial.println("Start Impulse ...");
      wasPlaying = true;
      playingSample = 0;
    }

    // Play noise from buffer A
    if (playingSample < IBUFFER_SIZE) {
      analogWrite(2, impulseBuffer[playingSample] / 16 + 2048); // Output audio data as PWM signal to pin A0
      delayMicroseconds(sampling_period_us); // 62.5); // Wait for 1/16000s (62.5us) for 16000Hz sample rate
      playingSample ++;

      if (playingSample >= IBUFFER_SIZE) {
        isPlaying = false;
      }
    } 

  } else {
    if(wasPlaying){
      Serial.println("... end Impulse.");
      wasPlaying = false;
    }
  }
}



void takeSamplesA() { // TODO Clean
  // for (int i = 0; i < SAMPLES; i++) {
  //   unsigned long newTime = micros();
  //   int value = analogRead(A0);
  //   vReal[i] = value;
  //   vImag[i] = 0;
  //   while (micros() < (newTime + sampling_period_us)) {
  //     yield();
  //   }
  // }
}

void takeSamplesPDM() { // PDM lib version // TODO Clean

    // if ( samplesReaded < MAX_REC_SAMPLES ) {

    //   if( !isRecording ){
    //     isRecording = true;
    //   }

    //   int bytesAvailable = PDM.available();
    //   if ((samplesReaded + bytesAvailable/2 ) > MAX_REC_SAMPLES) {
    //     bytesAvailable = (MAX_REC_SAMPLES - samplesReaded) * 2;
    //   } else if( bytesAvailable < 2 ){
    //     delayMicroseconds(sampling_period_us);
    //     continue;
    //   }

    //   double tempB[MAX_REC_SAMPLES];
    //   int bytesRead = PDM.read(tempB, bytesAvailable);
    //   for (int i = samplesReaded; i < (samplesReaded + bytesAvailable/2); i++) {
    //     int index = i - samplesReaded;
    //     vReal[i] = tempB[index];
    //     vImag[i] = 0;
    //   }

    //   samplesReaded += bytesRead/2; // 16-bit, 2 bytes per sample
    
    // } else {

    //   if ( isRecording ) {
    //     isRecording = false;
    //   }

    // }
  
}


void takeSamplesPDMParallel() { // PDM lib version

  if (isRecording) {
    if (!wasRecording) {
      Serial.println("Start recording ...");
      wasRecording = true;
      readingSample = 0;
    }

    if ( readingSample < MAX_REC_SAMPLES ) {

      int bytesAvailable = PDM.available();
      if ((readingSample + bytesAvailable/2 ) > MAX_REC_SAMPLES) {
        bytesAvailable = (MAX_REC_SAMPLES - readingSample) * 2;
      } else if( bytesAvailable < 2 ){
        // delayMicroseconds(sampling_period_us);
        // skip rest of the function
        Serial.println("Recording: No samples available.");
        return;
      }

      double tempBuffer[MAX_REC_SAMPLES];
      int bytesRead = PDM.read(tempBuffer, bytesAvailable);
      for (int i = readingSample; i < (readingSample + bytesAvailable/2); i++) {
        int index = i - readingSample;
        vReal[i] = tempBuffer[index];
        vImag[i] = 0;
        Serial.print( "Recorded byte: " );
        Serial.println( String(tempBuffer[index]) );
      }

      readingSample += bytesRead/2; // 16-bit, 2 bytes per sample
      
      if ( readingSample >= MAX_REC_SAMPLES ) {
        isRecording = false;
        isIRon = false;
      }
    
    }

  } else {
    if (wasRecording) {
      Serial.println("... end recording.");
      wasRecording = false;
      //doProcessProfile = true;
    }
  }
  
}


void computeFFT() {
  // compute FFT
  fft.DCRemoval();
  fft.Windowing(FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  fft.Compute(FFT_FORWARD);
  fft.ComplexToMagnitude();

  double median[20];
  double max[20];
  int index = 0;
  double hzPerSample = (1.0 * SAMPLING_FREQ) / SAMPLES; //
  double hz = 0;
  double maxinband = 0;
  double sum = 0;
  int count = 0;

  for (int i = 2; i < (SAMPLES / 2) ; i++) {
    count++;
    sum += vReal[i];
    if (vReal[i] >  max[index] ) {
      max[index] = vReal[i];
    }
    if (hz > coutoffFrequencies[index]) {
      median[index] = sum / count;
      sum = 0.0;
      count = 0;
      index++;
      max[index] = 0;
      median[index]  = 0;
    }
    hz += hzPerSample;
  }
  // calculate median and maximum per frequency band
  if ( sum > 0.0) {
    median[index] =  sum / count;
    if (median[index] > maxinband) {
      maxinband = median[index];
    }
  }
}

