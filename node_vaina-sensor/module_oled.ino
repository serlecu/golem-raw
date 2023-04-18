void setupOLED() {
  display.clearDisplay();
}

void handleOLED() {
    // Clear the display
  display.clearDisplay();
  
  display.drawRect(2, int(display.height()/2), display.width()-2, display.height()-2, SSD1306_WHITE);
  notifyBadge(12, 24, 6 );
  headerText(BLE.address());

  //scrollingMAC();
  display.display();

  if( displayErrorOLED > 0 ) {
    errorOLED(displayErrorOLED);
  }
}

void notifyBadge(int16_t posX, int16_t posY, int16_t radius) {
  if ( justNotified > 0 ) { // contador de ciclos
    circleFilled(posX, posY, radius);
    justNotified --;
  } else {
    circleOutline(posX, posY, radius);
  }
  //display.display();
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

void errorOLED(int error) {
  // Draw an ALERT ICON
}