void handleOLED() {
    // Clear the display
  display.clearDisplay();
  
  display.drawRect(2, int(display.height()/2), display.width()-2, display.height()-2, SSD1306_WHITE);
  notifyBadge(16, 24, 8 );
  scrollingMAC();
  

  //display.display();
}

void notifyBadge(int16_t posX, int16_t posY, int16_t radius) {
  if ( justNotified > 0 ) { // contador de ciclos
    circleFilled(posX, posY, radius);
    justNotified --;
  } else {
    circleOutline(posX, posY, radius);
  }
}

void circleOutline(int16_t posX, int16_t posY, int16_t radius) {
    display.drawCircle(posX, posY, radius, SSD1306_WHITE);
}

void circleFilled(int16_t posX, int16_t posY, int16_t radius) {
  for(int16_t i= radius; i>0; i-=3) {
    // The INVERSE color is used so circles alternate white/black
    display.fillCircle(posX, posX, i, SSD1306_INVERSE);
    display.display(); // Update screen with each newly-drawn circle
  }
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