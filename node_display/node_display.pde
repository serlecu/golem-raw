boolean bgFadeDir = true;
int bgColour = 125;
int pointPosX = 200;
int pointPosY = 200;

void setup(){
 size(480,480);
 
 roundBackground(bgColour);
}

void draw(){
  if(bgFadeDir) {
    bgColour ++;
    if(bgColour >= 205){
      bgFadeDir = false;
    }
  } else {
    bgColour --;
    if(bgColour <= 50){
      bgFadeDir = true;
    }
  }
  roundBackground(bgColour);
  if(mouseX > 50 && mouseX < 430){
    pointPosX = mouseX;
  }
  if (mouseY > 50 && mouseY < 430){  
    pointPosY = mouseY;
  }
  
  fill(0);
  ellipse(pointPosX,pointPosY,100,100);
}

void roundBackground(int gray){
  fill(gray,gray,gray);
  noStroke();
  ellipse(240,240,480,480);
}  

void keyPressed(){
  if(key == 'q' || key == 'Q'){
    exit();
  }
}
