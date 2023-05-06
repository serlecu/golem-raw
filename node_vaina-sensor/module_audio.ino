// ====== IN SETUP ======
bool startedPDM = false;

bool setupIR() {

  PDM.onReceive(onPDMdata);
  PDM.setBufferSize(128);

  if (!PDM.begin(1, 16000)) {
    errorOLED(30);
    Serial.println("Failed to start PDM!");
    return false;
  } else {
    startedPDM = true;
  }
  
  // -- IMPULSE --
  // change pwm output freq for PWM_A
   PWM_A.period(1.0/20000.0); // was 200k, I'm testing 32k80 for a 16k SampleRat
  // Start the Threads
  impulseThread.start( playImpulseThreadedLoop );

  // -- FFT & PROFILE --
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
void handleIR(bool canRun) {
  if ( canRun ) {

    if ( isIRon ) {

      takeSamplesPDMParallel();
      computeFFT();

    } else {
      if ( (millis() - IRtimer) > AUDIO_IMPULSE_FREQ ) {
        launchIR = NOTIFICATION_BADGE_DECAY; // bang in OLED
        
        isIRon = true; // flag for start IR routine
        //isPlaying = true;
        canPlay = true;
        isRecording = true;
          
        IRtimer = millis();
      }
    }

  }
}


// ====== FUNCTIONS ======

void outputSample() {
    // PWM_A = (float)(moogTest[playingSample] + 128) / 255; // buffer size = 512
    PWM_A = (float)(noiseBuffer[playingSample] + 128) / 255.0;
    playingSample = (playingSample + 1) % IBUFFER_SIZE;
}

void playImpulseThreadedLoop() {
  // Serial.println("Impulse Thread Started"); 
  unsigned long playbackTimer;

  while(1){
    if (canPlay){
      isPlaying = true;
      playbackTimer = millis();
      Serial.println("Start Impulse ...");

      playingSample = 0;
      // audioTicker.attach(&outputSample, 1.0 / 16000.0);

      while ( (millis() - playbackTimer) < IBUFFER_MILLIS ){
        Serial.println(String((millis() - playbackTimer))+" / "+String(IBUFFER_MILLIS));
        rtos::ThisThread::sleep_for(20);
      }

      // audioTicker.detach();
      // analogWrite(2, -1);
      // PWM_A = 0.0;

      Serial.println("... end Impulse.");
      isPlaying = false;
      canPlay = false;
    }
  }
}


// Record
void takeSamplesPDMParallel() { // PDM lib version
  if (isRecording) {
    if (!wasRecording) {
      Serial.println("Start recording ...");
      if (! startedPDM ) {
        errorSequence(3);
        Serial.println("PDM needs reboot");
      }
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
        return;
      }

      int totalSamples = readingSample + freshSamplesChecked;
      for (int i = readingSample; i < totalSamples-1; i++) {
        int index = i - readingSample;
        // Serial.println("InLoop: "+String(i)+"/"+String(totalSamples));

        if (tempBuffer[index] != '-nan'){
          vReal[i] = tempBuffer[index];
          vImag[i] = 0;
          // Serial.println( "Recorded byte: "+String(tempBuffer[index]) );

        } else {
          totalSamples = i;
          Serial.println( "Unexpected end" );
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

// Compute Profile
void computeFFT() {
  switch (isIRprocessing) {
    case 1:
      Serial.println("Start Processing!");
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
        resultsFFT[index] = median[index]; 
      }

      Serial.println("Done Processing!");
      // for (int i = 0; i < FREQUENCY_BANDS; i++) {
      //    Serial.print( String(median[i])+", ");
      // }
      // Serial.println("end.");

      IRupdated = true;
      isIRprocessing = 0;
      isIRon = false;

      break;
  }

}

// GET AUDIO DATA
// callback / ISR process
void onPDMdata() {
      int bytesAvailable = PDM.available();

      PDM.read(tempBuffer, bytesAvailable);

      freshSamples = bytesAvailable / 2; // 16-bit, 2 bytes per sample
}