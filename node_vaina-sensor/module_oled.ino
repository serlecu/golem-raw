void setupOLED() {
  display.clearDisplay();
}

void handleOLED() {
  if( displayErrorOLED > 0 ) {
    errorOLED(displayErrorOLED);

  } else {
    // Clear the display
    display.clearDisplay();

    display.drawRect(2, int(display.height()/2), display.width()-2, display.height()-2, SSD1306_WHITE);
    
    notifyBadge(12, 24, 6, launchIR);
    statusBadge(28, 24, 6, isIRon ); //Playing
    statusBadge(40, 24, 6, isPlaying ); //Playing
    statusBadge(52, 24, 6, isRecording ); //Recording
    statusBadge(64, 24, 6, (isIRprocessing > 0) ); //Recording
    
    notifyBadge(84, 24, 6, justNotified);

    headerText(BLE.address());

    //scrollingMAC();
    display.display();
  }
}

void statusBadge(int16_t posX, int16_t posY, int16_t radius, bool listener) {
  if ( listener ) {
    circleFilled(posX, posY, radius);
  } else {
    circleOutline(posX, posY, radius);
  }
}

void notifyBadge(int16_t posX, int16_t posY, int16_t radius, int listener) {
  if ( listener > 0 ) { // contador de ciclos
    circleFilled(posX, posY, radius);
    listener --;
  } else {
    circleOutline(posX, posY, radius);
  }
}

void circleOutline(int16_t posX, int16_t posY, int16_t radius) {
  int16_t outline = 1;
    display.fillCircle(posX, posY, radius, SSD1306_WHITE);
    display.fillCircle(posX, posY, radius-outline, SSD1306_BLACK);
}

void circleFilled(int16_t posX, int16_t posY, int16_t radius) {
  int16_t outline = 1;
  display.fillCircle(posX, posY, radius, SSD1306_WHITE);//SSD1306_INVERSE);
  display.fillCircle(posX, posY, radius-outline, SSD1306_BLACK);
  display.fillCircle(posX, posY, 2, SSD1306_WHITE);//SSD1306_INVERSE);
  // for(int16_t i= radius; i>0; i-=1) {
    // The INVERSE color is used so circles alternate white/black
    // display.fillCircle(posX, posX, i, SSD1306_WHITE);//SSD1306_INVERSE);
    // display.display(); // Update screen with each newly-drawn circle
  // }
}

void headerText(String text) {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println(text);
}

void scrollingMAC() {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println(BLE.address());
  if (!isMacScrolling){
    display.display();
    display.startscrollright(0x00, 0x00);
    isMacScrolling = true;
  }
}

static const unsigned char PROGMEM bitmapAlert[] = // 128x32px
{	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x60, 0x38, 0x08, 
	0x08, 0x18, 0x60, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0xe0, 0x30, 0x0c, 0x07, 0x01, 0x00, 0x00, 0xf0, 
	0xf0, 0x00, 0x00, 0x01, 0x07, 0x0c, 0x30, 0xe0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0xc0, 0x70, 0x1c, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xcf, 
	0xcf, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x06, 0x1c, 0x70, 0xc0, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x1e, 0x13, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 
	0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x13, 0x1e, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

void errorOLED(int error) {
  display.clearDisplay();
  // Draw an ALERT ICON
  display.drawGrayscaleBitmap(0, 0, bitmapAlert, 128, 32);
  // Print Error Code
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println("Error: "+String(error));
  //
  display.display();
}