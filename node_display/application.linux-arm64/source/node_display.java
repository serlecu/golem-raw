import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class node_display extends PApplet {

boolean bgFadeDir = true;
int bgColour = 125;
int pointPosX = 200;
int pointPosY = 200;

public void setup(){
 
 
 roundBackground(bgColour);
}

public void draw(){
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

public void roundBackground(int gray){
  fill(gray,gray,gray);
  noStroke();
  ellipse(240,240,480,480);
}  

public void keyPressed(){
  if(key == 'q' || key == 'Q'){
    exit();
  }
}
  public void settings() {  size(480,480); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "--present", "--window-color=#666666", "--hide-stop", "node_display" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
