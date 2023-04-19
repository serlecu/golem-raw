// ====== IN SETUP ======
bool setupIR() {
  pinMode(PWM_PIN_A, OUTPUT);
  pinMode(PWM_PIN_B, OUTPUT);

  PDM.onReceive(onPDMdata);
  PDM.setBufferSize(128);

  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to start PDM!");
    return false;
  }

  sampling_period_us = (1.0 / SAMPLING_FREQ ) * pow(10.0, 6);

  // Calculate cuttoff frequencies,meake a logarithmic scale base basePOt
  double basePot = pow(SAMPLING_FREQ / 2.0, 1.0 / FREQUENCY_BANDS);
  coutoffFrequencies[0] = basePot;
  for (int i = 1 ; i < FREQUENCY_BANDS; i++ ) {
    coutoffFrequencies[i] = basePot * coutoffFrequencies[i - 1];
  }

  // Fill resoultsFFT with -nan
  for (int i = 1 ; i < FREQUENCY_BANDS; i++ ) {
    resultsFFT[i] = '-nan';
  }
}


// ======= IN LOOP =======
void handleIR() {

  if ( isIRon ) {
    // playImpulseParallel();
    takeSamplesPDMParallel();
    computeFFT();
    // processIRProfile();

  } else {
    if ( (millis() - IRtimer) > AUDIO_IMPULSE_FREQ ) {
      launchIR = NOTIFICATION_BADGE_DECAY; // bang in OLED
      
      isIRon = true; // flag for start IR routine
      isPlaying = true;
      isRecording = true;
      //impulseThread->start(playImpulseThreaded);
      //recordingThread.start();
      
      Serial.println(String(millis()-IRtimer) + " > " + String(AUDIO_IMPULSE_FREQ));
      IRtimer = millis();
    }
  }

}


// ====== FUNCTIONS ======
bool createImpulse() {
  for (int i = 0; i < IBUFFER_SIZE; i++) {
    // Generate random noise data between -32768 and 32767
    // impulseBufferA[i] = double(random(-32768, 32767));
    // impulseBufferB[i] = double(random(-32768, 32767));
    impulseBufferA[i] = (double)map(i,0,IBUFFER_SIZE, -32768, 32767) ;
    impulseBufferB[i] = (double)map(i,0,IBUFFER_SIZE, -32768, 32767) ;
  }
  return true;
}

// PLAY IMPULSE
void playImpulse() {
  Serial.println("Start Impulse ...");
  // Play noise from buffer A
  for (int i = 0; i < IBUFFER_SIZE; i++) {
    Serial.println("Loop: "+String(i)+" / "+String(IBUFFER_SIZE));
    analogWrite(PWM_PIN_A, impulseBufferA[playingSample] / 16 + 2048);
    analogWrite(PWM_PIN_B, impulseBufferB[playingSample] / 16 + 2048);
    //delayMicroseconds(sampling_period_us);// 62.5); // Wait for 1/16000s (62.5us) for 16000Hz sample rate
  }
  Serial.println("... end Impulse.");
}
void playImpulseThreaded() {
  Serial.println("Start Impulse ...");

  // Play noise from buffer A
  for (int i = 0; i < IBUFFER_SIZE/2; i++) {
    Serial.println("Loop: "+String(i)+" / "+String(IBUFFER_SIZE));

    int headB = playingSample + IBUFFER_SIZE/2;
    analogWrite(PWM_PIN_A, impulseBufferA[playingSample] / 16 + 2048);
    analogWrite(PWM_PIN_B, impulseBufferA[headB] / 16 + 2048);
    rtos::ThisThread::sleep_for(1);
    //delayMicroseconds(sampling_period_us);// 62.5); // Wait for 1/16000s (62.5us) for 16000Hz sample rate
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
    if (playingSample < IBUFFER_SIZE/2) {
      Serial.println("Loop: "+String(playingSample)+" / "+String(IBUFFER_SIZE));
      int headB = playingSample + IBUFFER_SIZE/2;
      analogWrite(PWM_PIN_A, impulseBufferA[playingSample] / 16 + 2048);
      analogWrite(PWM_PIN_B, impulseBufferA[headB] / 16 + 2048);
      // analogWrite(PWM_PIN_B, impulseBufferB[playingSample] / 16 + 2048);
      //delayMicroseconds(sampling_period_us); // 62.5); // Wait for 1/16000s (62.5us) for 16000Hz sample rate
      playingSample ++;

      if (playingSample >= IBUFFER_SIZE) {
        isPlaying = false;
        analogWrite(PWM_PIN_A, 0);
        analogWrite(PWM_PIN_B, 0);
      }
    } 

  } else {
    if(wasPlaying){
      Serial.println("... end Impulse.");
      wasPlaying = false;
    }
  }
}

// RECORD
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
      // Serial.println("FreshSamples: "+String(freshSamples));
      int freshSamplesChecked = freshSamples;

      // Check & Limit ammout of samples to append
      if ((readingSample + freshSamples ) > MAX_REC_SAMPLES) {
        freshSamplesChecked = (MAX_REC_SAMPLES - readingSample);
        // Serial.println("GO! "+ String(freshSamplesChecked));

      } else if( freshSamples < 1 ){
        Serial.println("Recording: No samples available.");
        //delayMicroseconds(sampling_period_us); // 62.5); // Wait for 1/16000s (62.5us) for 16000Hz sample rate
        return;
      }

      int totalSamples = readingSample + freshSamplesChecked;
      for (int i = readingSample; i < totalSamples-1; i++) {
        int index = i - readingSample;
        Serial.println("InLoop: "+String(i)+"/"+String(totalSamples));

        if (tempBuffer[index] != '-nan'){
          vReal[i] = tempBuffer[index];
          vImag[i] = 0;
          // Serial.println( "Recorded byte: "+String(tempBuffer[index]) );

        } else {
          totalSamples = i;
          // Serial.println( "Unexpected end" );
          break;
        }
      }

      readingSample = totalSamples; 
      // Serial.println("Samples: "+String(readingSample)+"/"+String(MAX_REC_SAMPLES));
      
      if ( readingSample >= MAX_REC_SAMPLES ) {
        isRecording = false;
      }

    }

  } else {
    if (wasRecording) {
      Serial.println("... end recording.");
      wasRecording = false;
      isIRprocessing = 1;
    }
  }
  
}

// PROFILE
void computeFFT() {
  switch (isIRprocessing) {
    case 1:
      // compute FFT
      fft.DCRemoval();
      fft.Windowing(FFT_WIN_TYP_HAMMING, FFT_FORWARD);
      fft.Compute(FFT_FORWARD);
      fft.ComplexToMagnitude();
      isIRprocessing ++;
      break;

    case 2:
      double median[FREQUENCY_BANDS];
      double max[FREQUENCY_BANDS];
      int index = 0;
      double hzPerSample = (1.0 * SAMPLING_FREQ) / SAMPLES; //
      double hz = 0;
      double maxinband = 0;
      double sum = 0;
      int count = 0;

      // Do what?
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

      Serial.println("Done Processing!");
      for (int i = 0; i < FREQUENCY_BANDS; i++) {
         Serial.print( String(median[i])+", ");
      }
      Serial.println("end.");

      resultsFFT = median;
      IRupdated = true;
      isIRprocessing = 0;
      isIRon = false;

      break;
  }

}

// GET AUDIO DATA
// callback / IRS process
void onPDMdata() {
      int bytesAvailable = PDM.available();

      PDM.read(tempBuffer, bytesAvailable);

      freshSamples = bytesAvailable / 2; // 16-bit, 2 bytes per sample
}